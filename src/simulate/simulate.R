# user
library(data.table)

set.seed(1234)

N_users = 1000

# load artist and song names
artists <- fread('../../data/apis-to-scrape-artists.csv')
artists[, sampled:=runif(.N)]
artist_names = artists[sampled<=.05]$artist_name
artist_popularity = runif(length(artist_names))

# artist and song names
dates = seq(from=as.Date('2023-01-01'), to = as.Date('2023-01-02'), by = '1 day') #12-31'), by = '1 day')

usernames = paste0('user', 1:N_users)
user_active = runif(length(usernames)) # probability that a user, on any given day listens
usage_intensity = rpois(length(usernames), 12) # approximate number of songs consumed

# simulate data
song_lengths = seq(from=180, to=240, by = 1)

history = rbindlist(lapply(usernames, function(user) {
  rbindlist(lapply(dates, function(date) {
    # play music?
    play = runif(1)<=user_active[which(user==usernames)]
    if (play==FALSE) return(list())
    
    # which artists get consumed?
    nsongs = max(1,rpois(1,usage_intensity[which(user==usernames)]))
    artists = sample(artist_names, nsongs, prob=artist_popularity)
    
    # listening offset: when does the session start?
    offset = as.numeric(sample(seq(as.POSIXct(date), as.POSIXct(date+1), by="1 mins"),1))
    
    
    unix = cumsum(c(offset, sample(song_lengths, nsongs-1)))
      
    usage = data.table(user = user, date = date, timestamp = unix, artist=artists, track = 'emptytrack')
    return(usage)
  }))
}))

# create user demo
set.seed(1234)
users = data.table(username=usernames)[, age := rpois(.N, 35)][, country:=sample(c('DE', 'NL', 'BE'), .N, replace=T)]
users[, description:='none']


fwrite(history, '../../listening.csv')
fwrite(users, '../../users.csv')





