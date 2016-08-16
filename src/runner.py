import connection
import os
import logging
import time
from imageAnalyzer import ImageAnalyzer

DIRECTORY = 'photos/'
IMAGEA = 'a.jpg'
IMAGEB = 'b.jpg'
SUBREDDIT = 'earthporn'
CONFIGURATION = 'conf.info'
DATETIME = time.strftime("%Y-%m-%d") + '.' + time.strftime("%H.%M.%S")
logging.basicConfig(filename=str('logs/' + DATETIME + ".log"), level=logging.DEBUG)
logger = logging.getLogger('redditdesktop.runner')
prevImageLink = open(DIRECTORY + CONFIGURATION).read().rstrip()

print('scraping r/' + SUBREDDIT + '...')
logger.info('scraping r/' + SUBREDDIT + '...')
post = connection.selectPicture('http://www.reddit.com/r/' + SUBREDDIT)

if post.link == prevImageLink:
    print('top image already set as wallpaper (' + post.link + ')')
else:
    print('downloading image...')
    logger.info('downloading image...')
    image = connection.downloadPicture(post)
    print('resizing image...')
    logger.info('resizing image...')
    analyzer = ImageAnalyzer(image)
    analyzer.cropToScreenRatio()
    analyzer.image.load()
    print('saving image...')
    logger.info('saving image...')
    os.remove(DIRECTORY + IMAGEA)
    analyzer.image.save(DIRECTORY + IMAGEA)
    os.remove(DIRECTORY + IMAGEB)
    analyzer.image.save(DIRECTORY + IMAGEB)
    print(post.link, file=open(DIRECTORY + CONFIGURATION, 'w'))
    print('done')
    logger.info('done')


