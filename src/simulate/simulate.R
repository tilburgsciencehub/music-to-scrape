# user
library(data.table)
library(DBI)
library(RSQLite)

set.seed(1234)
warning(getwd())
N_users = 500

# load artist and song names
raw <- fread("https://raw.githubusercontent.com/mahkaila/songnames/master/SongCSV.csv", quote="")

# remove any artist/song with wrongly encoded names
raw <- raw[!grepl('\\\\x', ArtistName)&!grepl('\\\\x',Title)]

# clean-up byte-look-alike strings
selected_cols = colnames(raw)[which(unlist(lapply(raw, class)=='character'))]
for (col in selected_cols) raw[, (col):=gsub("b['|\"]","", get(col))]
for (col in selected_cols) raw[, (col):=gsub("['|\"]$","", get(col))]
for (col in selected_cols) raw[, (col):=gsub('^["]',"", get(col))]
for (col in selected_cols) raw[, (col):=gsub("['|\"]$","", get(col))]

raw[Year==0, Year:=NA]


artists = unique(raw, by = c('ArtistID'))[, c('ArtistID','ArtistName','ArtistLocation'),with=F]
artists[, sampled:=runif(.N)]
artists[, popularity:=runif(.N)]

songs = unique(raw, by = c('SongID'))[, c('ArtistID','ArtistName','SongID','AlbumID','Danceability','Duration','KeySignature','Tempo','TimeSignature','Title', 'Year')]

setkey(songs, ArtistID)
setkey(artists, ArtistID)
songs[artists, artist_popularity:=i.popularity]

# set time horizon
dates = seq(from=as.Date('2022-12-01'), to = as.Date('2024-01-01'), by = '1 day')

usernames = paste0('user', 1:N_users)
user_active = runif(length(usernames)) # probability that a user, on any given day listens
usage_intensity = rpois(length(usernames), 12) # approximate number of songs consumed

# simulate data

history = rbindlist(lapply(usernames, function(user) {
  play = data.table(date=dates, active=runif(length(dates))<=user_active[which(user==usernames)])
  play[, nsongs:=pmax(1,rpois(.N,usage_intensity[which(user==usernames)]))]
  play[, date_unix:=as.numeric(as.POSIXct(date))]
  play[active==F, nsongs:=0]
  play[active==T, offset:=sample(0:(3600*24-1),.N)]
  play[active==T, timestamp_session_start:=date_unix+offset]
  # generate play timestamps
  
  timestamps = rep(play[active==T]$timestamp_session_start, play[active==T]$nsongs)
  my_dates = rep(play[active==T]$date, play[active==T]$nsongs)
  
  selected_songs=songs[match(sample(songs$SongID, sum(play[active==T]$nsongs), prob=songs$artist_popularity),SongID)]
  selected_songs[, date:=my_dates]
  selected_songs[, session_start_unix:=timestamps]
  
  selected_songs[, unix:=cumsum(c(session_start_unix[1], rev(rev(Duration)[-1]))), by = c('date')]
                
        
  usage = selected_songs[, list(user = user, date = date, timestamp = unix, 
                         artist_id=ArtistID, song_id = SongID, unique_id = paste0(unix,ArtistID,SongID))]
  
  return(usage)
  }))

history <- history[!is.na(date)]

# create user demo
set.seed(1234)
users = data.table(username=usernames)[, age := rpois(.N, 35)][, country:=sample(c('DE', 'NL', 'BE'), .N, replace=T)]
users[, description:='none']

# featured artists
artists[, featured:=runif(.N)<=.01]

artists[, ':=' (sampled=NULL, popularity=NULL)]

songs[, ':=' (artist_popularity=NULL)]

# Remove existing database files if they exist
db_file_fastapi <- "sql_app/apistoscrape.db"
if (file.exists(db_file_fastapi)) {
  file.remove(db_file_fastapi)
}

db_file_flask <- "flask_app/apistoscrape.db"
if (file.exists(db_file_flask)) {
  file.remove(db_file_flask)
}

# Convert the dates to character (string) format
history$date <- as.character(history$date)

#generate sqlite database for fastapi
con_fastapi <- dbConnect(RSQLite::SQLite(), dbname = "sql_app/apistoscrape.db")

dbWriteTable(con_fastapi, "users", users)
dbWriteTable(con_fastapi, "songs", songs)
dbWriteTable(con_fastapi, "artists", artists, field.types = c(featured = "TEXT"))
dbWriteTable(con_fastapi, "listening", history)

dbDisconnect(con_fastapi)

#generate sqlite database for fastapi
con_flask <- dbConnect(RSQLite::SQLite(), dbname = "flask_app/apistoscrape.db")

dbWriteTable(con_flask, "users", users)
dbWriteTable(con_flask, "songs", songs)
dbWriteTable(con_flask, "artists", artists, field.types = c(featured = "TEXT"))
dbWriteTable(con_flask, "listening", history, field.types = c(date = "TEXT"))

dbDisconnect(con_flask)


warning('Completed prepping database')
