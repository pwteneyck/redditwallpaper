import requests
import re
import ctypes
from redditHTML import RedditParser
from PIL import Image
from urllib import request
import time
import logging

logger = logging.getLogger('redditdesktop.connection')

def selectPicture(url):
    logger.info('wat')
    u = ctypes.windll.user32
    r = openURL(url)
    if r == None:
        logger.critical('empty request response')
    else:
        parser = RedditParser()
        parser.feed(r.text)
        post = parser.nextImagePost()
        screenWidth = u.GetSystemMetrics(0)
        screenHeight = u.GetSystemMetrics(1)
        while post.height < screenHeight or post.width < screenWidth:
            logger.info('post \"' + post.title + '\" is too small (screen size is ' + str(screenWidth) + 'x' + str(screenHeight) + ')')
            post = parser.nextImagePost()
        return post

def downloadPicture(redditImagePost):
    directory = 'C:/ProgramData/RedditWallpapers/history/'
    cleanedTitle = re.sub(r'[/\\:\*\?\"<>\|]', '', redditImagePost.title)
    cleanedTitle = re.sub(r'&quot;', '\'', cleanedTitle)
    filename = time.strftime("%Y-%m-%d") + '.' + time.strftime("%H.%M.%S") + '; ' + cleanedTitle + '.jpg'
    request.urlretrieve(redditImagePost.link, directory + filename)
    i = Image.open(directory + filename)
    return i

def openURL(url, timeout=20):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'From': 'pwteneyck@gmail.com'
    }
    for i in range(0, timeout):
        try:
            r = requests.get(url, headers = HEADERS)
            return r
        except requests.exceptions.ConnectionError as e:
            print('\t connection failed. retrying...\t(' + str(i+1) + ')')
            logger.warning('connection failed:: ' + e.strerror)
            time.sleep(1)
    logger.critical('unable to establish connection to ' + url)
