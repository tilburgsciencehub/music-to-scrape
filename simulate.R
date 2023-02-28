# user
library(data.table)

set.seed(1234)

N_users = 1000

artist_names = paste0('artist', 1:200)
artist_popularity = runif(artist_names)

dates = seq(from=as.Date('2023-01-01'), to = as.Date('2023-01-02'), by = '1 day') #12-31'), by = '1 day')

usernames = paste0('user', 1:N_users)
user_active = runif(length(usernames)) # probability that a user, on any given day listens
usage_intensity = rpois(length(usernames), 12) # approximate number of songs consumed

# simulate data

history = rbindlist(lapply(usernames, function(user) {
  rbindlist(lapply(dates, function(date) {
    # play music?
    play = runif(1)<=user_active[which(user==usernames)]
    if (play==FALSE) return(list())
    
    # which artists get consumed?
    nsongs = max(1,rpois(1,usage_intensity[which(user==usernames)]))
    artists = sample(artist_names, nsongs, prob=artist_popularity)
    
    usage = data.table(user = user, date = date, timestamp = 12345678, artist=artists, track = 'emptytrack')
    return(usage)
  }))
}))

# main data


# by user and week: user
history[, list(plays=.N), by = c('user')]
# by day
history[, list(plays=.N), by = c('date')]
# by artist
history[, list(plays=.N), by = c('artist')] %>% arrange(desc(plays))


# next steps:

# 1) endpoints

# sample user names (reveiling different user names with some attributes)
usernames_shuffled = usernames[order(runif(length(usernames)))]
usernames_shuffled[1:10] # w/ limit page...
usernames_shuffled[2:20]

# --> total plays, bigrapphy, mockup: 
# --> "view" --> "recently active users"

# 2) get.user_info

# aggregate stats by a user, most popular tracks, most popular artist
# mockup: https://www.last.fm/user/ALUSER

# 3) get.user_plays (listening history)
 # default is one week
# arguments: beginning date, end date; pagination

history

# get_artist_info

# get_artist_plays



