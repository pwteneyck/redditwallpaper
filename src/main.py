import connection

SUBREDDIT = 'earthporn'

print('scraping r/' + SUBREDDIT + '...')
post = connection.selectPicture('http://www.reddit.com/r/' + SUBREDDIT)
print(post.title)