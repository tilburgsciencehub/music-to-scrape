# user
library(data.table)
library(DBI)
library(RSQLite)

set.seed(1234)
# warning(getwd())
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
dates = seq(from=as.Date('2023-12-01'), to = as.Date('2026-01-01'), by = '1 day')

# generate user names
generate_fake_usernames <- function(num_usernames = 1000, min_word_length = 5, max_word_length = 10, num_numbers = 2) {
  # Define a list of random words or fragments
  words <- c("Gamer", "Ninja", "Coder", "Geek", "Panda", "Cyber", "Pixel", "Rocket", "Wizard", "Dragon", "Star", "Cosmic", "Moon", "Tech", "Sonic", "Galaxy", "Stealth", "Shadow", "Vector")

  # Initialize an empty vector to store generated usernames
  usernames <- character(0)

  # Generate the specified number of usernames
  for (i in 1:num_usernames) {
    # Randomly select words and numbers to create a username
    username_parts <- sample(words, sample(min_word_length:max_word_length, 1))
    username_parts <- c(username_parts, sample(0:9, num_numbers))

    # Combine the selected parts into a single username
    username <- paste(username_parts, collapse = "")

    # Append the username to the vector
    usernames <- c(usernames, username)
  }

  return(usernames)
}

# Generate 1000 fake usernames; hard-code starcoder49 so it can be used in my tutorials.
set.seed(1234)
fake_usernames <- unique(c('StarCoder49', generate_fake_usernames(num_usernames = floor(1000*1.2), min_word_length=1, max_word_length = 2)))

usernames = fake_usernames[1:N_users] #paste0('user', 1:N_users)
user_active = runif(length(usernames), min = .1, max=1) # probability that a user, on any given day listens
usage_intensity = rpois(length(usernames), 12) # approximate number of songs consumed

# simulate data
history = rbindlist(lapply(usernames, function(user) {
  play <- data.table(date=dates, active=runif(length(dates))<=user_active[which(user==usernames)])
  play[, nsongs:=pmax(1,rpois(.N,usage_intensity[which(user==usernames)]))]
  play[, date_unix:=as.numeric(as.POSIXct(date))]
  play[active==F, nsongs:=0]
  play[active==T, offset:=sample(0:(3600*24-1),.N)]
  play[active==T, timestamp_session_start:=date_unix+offset]
  # generate play timestamps

  timestamps = rep(play[active==T]$timestamp_session_start, play[active==T]$nsongs)
  my_dates = rep(play[active==T]$date, play[active==T]$nsongs)

  selected_songs=songs[match(sample(songs$SongID, sum(play[active==T]$nsongs), prob=songs$artist_popularity, replace=T),SongID)]

  stopifnot(nrow(selected_songs)>0)
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

# For now just create indices on all fields.
# Probably overkill but at least it's somewhat future-proof.
# More careful query analysis might prove some of these indices
# redundant and perhaps inspire some additional multi-column indices.
primary_keys <- list(
  c("users", "username"),
  c("songs", "SongID"),
  c("artists", "ArtistID"),
  c("listening", "unique_id")
)

indices <- list(
  list("users", c("age", "country", "description")),
  list("songs", c(
    "ArtistID",
    "ArtistName",
    "AlbumID",
    "Danceability",
    "Duration",
    "KeySignature",
    "Tempo",
    "TimeSignature",
    "Title",
    "Year"
  )),
  list("artists", c(
    "ArtistName",
    "ArtistLocation",
    "featured"
  )),
  list("listening", c(
    "user",
    "date",
    "timestamp",
    "artist_id",
    "song_id"
  ))
)

add_indices <- function(con) {
  for (pkey in primary_keys) {
    table <- pkey[[1]]
    field <- pkey[[2]]

    dbExecute(con, sprintf("CREATE UNIQUE INDEX %1$s_%2$s ON %1$s (%2$s)", table, field))
  }

  for (index in indices) {
    table <- index[[1]]
    fields <- index[[2]]

    for (field in fields) {
      dbExecute(con, sprintf("CREATE INDEX %1$s_%2$s ON %1$s (%2$s)", table, field))
    }
  }
}

#generate sqlite database for fastapi
con_fastapi <- dbConnect(RSQLite::SQLite(), dbname = "sql_app/apistoscrape.db")

dbWriteTable(con_fastapi, "users", users)
dbWriteTable(con_fastapi, "songs", songs)
dbWriteTable(con_fastapi, "artists", artists, field.types = c(featured = "TEXT"))
dbWriteTable(con_fastapi, "listening", history)

add_indices(con_fastapi)

dbDisconnect(con_fastapi)

#generate sqlite database for flask
con_flask <- dbConnect(RSQLite::SQLite(), dbname = "flask_app/apistoscrape.db")

dbWriteTable(con_flask, "users", users)
dbWriteTable(con_flask, "songs", songs)
dbWriteTable(con_flask, "artists", artists, field.types = c(featured = "TEXT"))
dbWriteTable(con_flask, "listening", history, field.types = c(date = "TEXT"))

dbExecute(con_flask, "CREATE INDEX listening_user_timestamp ON listening (user, timestamp)")

add_indices(con_flask)

dbDisconnect(con_flask)


warning('Completed prepping database')
