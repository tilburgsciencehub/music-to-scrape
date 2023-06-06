# user
library(data.table)
library(DBI)
library(RSQLite)

set.seed(1234)
warning(getwd())
N_users = 1000

# load artist and song names
raw <- fread('https://raw.githubusercontent.com/mahkaila/songnames/master/SongCSV.csv')

for (col in colnames(raw)[which(unlist(lapply(raw, class)=='character'))]) raw[, (col):=gsub("b['|\"]","", get(col))]
for (col in colnames(raw)[which(unlist(lapply(raw, class)=='character'))]) raw[, (col):=gsub("['|\"]$","", get(col))]
raw[Year==0, Year:=NA]


#artists <- fread('../../data/apis-to-scrape-artists.csv')
artists = unique(raw, by = c('ArtistID'))[, c('ArtistID','ArtistName','ArtistLocation'),with=F]
artists[, sampled:=runif(.N)]
#artist_names = artists[sampled<=.05]$ArtistName
artists[, popularity:=runif(.N)]

songs = unique(raw, by = c('SongID'))[, c('ArtistID','ArtistName','SongID','AlbumID','Danceability','Duration','KeySignature','Tempo','TimeSignature','Title', 'Year')]

setkey(songs, ArtistID)
setkey(artists, ArtistID)
songs[artists, artist_popularity:=i.popularity]

# artist and song names
dates = seq(from=as.Date('2023-01-01'), to = as.Date('2023-06-01'), by = '1 day') #12-31'), by = '1 day')

usernames = paste0('user', 1:N_users)
user_active = runif(length(usernames)) # probability that a user, on any given day listens
usage_intensity = rpois(length(usernames), 12) # approximate number of songs consumed

# simulate data
# song_lengths = seq(from=180, to=240, by = 1)

history = rbindlist(lapply(usernames, function(user) {
  rbindlist(lapply(dates, function(date) {
    # play music?
    play = runif(1)<=user_active[which(user==usernames)]
    if (play==FALSE) return(list())
    
    # which artists get consumed?
    nsongs = max(1,rpois(1,usage_intensity[which(user==usernames)]))
    selected_songs=songs[match(sample(songs$SongID, nsongs, prob=songs$artist_popularity),SongID)]
    
    # listening offset: when does the session start?
    offset = as.numeric(sample(seq(as.POSIXct(date), as.POSIXct(date+1), by="1 mins"),1))
    
    unix = cumsum(c(offset, rev(rev(selected_songs$Duration)[-1])))
      
    usage = data.table(user = user, date = date, timestamp = unix, artist_id=selected_songs$ArtistID, song_id = selected_songs$SongID, unique_id = paste0(unix,selected_songs$ArtistID,selected_songs$SongID))
    return(usage)
  }))
}))

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
