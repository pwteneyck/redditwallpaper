import re
import logging
from html.parser import HTMLParser

dimensions = r".*\[([0-9]+) *[x×] *([0-9]+)\].*"

class RedditParser(HTMLParser):
    'parses through html and creates RedditPosts'
    POST_CLASS = '<div class=\"entry unvoted\"'
    currentIndex = 0
    inRedditPost = False
    currentLink = ''
    posts = []

    """
    create a RedditParser to parse through the given text (which *should be* HTML)
    WARNING: this is so poorly implemented that it hurts to document it.  Needs to be replaced
    unfortunately, BeautifulSoup doesn't work for Python 3.5 and I didn't feel like writing
    my own implementation of html.parser.  That should probably happen sooner or later, though
    """
    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if attrs[0][0] == 'class' and attrs[0][1] == 'entry unvoted':
                self.inRedditPost = True
        elif self.inRedditPost and tag == 'a':
            self.currentLink = attrs[1][1]

    def handle_data(self, data):
        if self.inRedditPost:
            self.posts.append(RedditPost(data, self.currentLink))
            self.inRedditPost = False

        """
        self.currentIndex = self.text.find(self.POST_CLASS, self.currentIndex)
        post = RedditPost(self.text[self.currentIndex:])
        self.currentIndex+=1
        return post
        """

    def nextImagePost(self):
        post = self.posts[self.currentIndex]
        while not (post.isPicture()):
            self.currentIndex += 1
            post = self.posts[self.currentIndex]
        self.currentIndex += 1
        return RedditImagePost(post.title, post.link)

class RedditPost:
    'An object containing the different html fields outlined in a single post on Reddit.  Very minimal for now'
    title = ''
    link = ''
    logger = logging.getLogger('redditdesktop.redditHTML.RedditPost')

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def isPicture(self):
        hasDimensions = re.match(dimensions, self.title)
        isDirectLink = re.match(r".*\.jpg", self.link)
        if not hasDimensions:
            return False
        if not isDirectLink:
            self.logger.warning('image post ignored; no direct link to .jpg :: ' + self.link)
            return False
        return True

class RedditImagePost:
    'An image post from a NoSillySuffix subreddit'
    title = ''
    link = ''
    width = 0
    height = 0

    def __init__(self, t, l):
        self.title = t
        self.link = l
        result = re.match(dimensions, self.title)
        self.width = int(result.group(1))
        self.height = int(result.group(2))
