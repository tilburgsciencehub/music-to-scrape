
# unique keys?
table(history[, list(N=.N),by=c('user','timestamp')]$N==1)
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

