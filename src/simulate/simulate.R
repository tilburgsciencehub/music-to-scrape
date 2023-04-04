# user
library(data.table)

set.seed(1234)

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
      
    usage = data.table(user = user, date = date, timestamp = unix, artist_id=selected_songs$ArtistID, song_id = selected_songs$SongID)
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

fwrite(artists, '../../artists.csv')
fwrite(songs, '../../songs.csv')
fwrite(history, '../../listening.csv')
fwrite(users, '../../users.csv')





