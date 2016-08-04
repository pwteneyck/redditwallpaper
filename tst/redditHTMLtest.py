import unittest
from random import randint
from redditHTML import RedditParser

class RedditParserTest(unittest.TestCase):
    REDDITPOST1 = '<div class=\"entry unvoted\"><p class=\"title\"><a class=\"title may-blank loggedin \" href=\"'
    REDDITPOST2 = '\" tabindex=\"1\" >'
    REDDITPOST3 = '</a>&#32;<span class=\"domain\">(<a href=\"/domain/esa.int/\">esa.int</a>)</span></p><p class=\"tagline\">submitted&#32;<time title=\"Tue Feb 2 12:08:43 2016 UTC\" datetime=\"2016-02-02T12:08:43+00:00\" class=\"live-timestamp\">7 hours ago</time>&#32;by&#32;<a href=\"\" ></a><span class=\"userattrs\"></span></p><ul class=\"flat-list buttons\"><li class=\"first\"><a href=\"\" class=\"comments may-blank\" >14 comments</a></li><li class=\"share\"><a class=\"post-sharing-button\" href=\"\"><a href=\"\">save</a></li><li><form action=\"/post/hide\" method=\"post\" class=\"state-button hide-button\"><input type=\"hidden\" name=\"executed\" value=\"hidden\" /><span><a href=\"\" class=\" \" onclick=\"\">hide</a></span></form></li><li class=\"report-button\"><a href=\"\" class=\"reportbtn access-required\" data-event-action=\"report\">report</a></li></ul><div class=\"reportform report-t3_43txqv\"></div><div class=\"expando\" style=\'display: none\' ><span class=\"error\">loading...</span></div></div><div class=\"child\" ></div><div class=\"clearleft\"></div></div><div class=\"clearleft\"></div><div class=\"\" id=\"\" onclick=\"\" data-fullname=\"t3_43qpah\" data-type=\"link\" data-author=\"\" data-author-fullname=\"\" data-subreddit=\"spaceporn\" data-subreddit-fullname=\"t5_2s9jc\" data-timestamp=\"1454361770000\" data-domain=\"\" ><p class=\"parent\"></p><span class=\"rank\">2</span><div class=\"midcol unvoted\" ><div class=\"arrow up login-required access-required\" data-event-action=\"upvote\" role=\"button\" aria-label=\"upvote\" tabindex=\"0\" ></div><div class=\"score dislikes\">1070</div><div class=\"score unvoted\">1071</div><div class=\"score likes\">1072</div><div class=\"arrow down login-required access-required\" data-event-action=\"downvote\" role=\"button\" aria-label=\"downvote\" tabindex=\"0\" ></div></div><a class=\"thumbnail may-blank loggedin \" href=\"\" ><img src=\"\" width=\'70\' height=\'47\' alt=\"\"></a>'

    html = ''
    posts = [] #contains (title, link) tuples
    images = [] #contains (title, link) tuples for image posts only

    def createredditpostHTML(self, isImage):
        name = 'wat' + randint(0,9)
        title = name
        if isImage:
            title += ' [' + randint(1,1000)
            if randint(0,1) == 0:
                title += ' x '
            else:
                title += 'x'
            title += randint(1,1000) + ']'
        return (title, name+'.jpg')

    def populatePosts(self, numposts):
        for i in range(numposts):
            post = None
            if randint(0,1) == 0:
                post = self.createredditpostHTML(True)
                self.images.append(post)
            self.posts.append(post)
            self.html += self.REDDITPOST1 + post[1] + self.REDDITPOST2 + post[0] + self.REDDITPOST3

    def setUp(self):
        self.populatePosts()

    def test(self):
        parser = RedditParser()
        parser.feed(self.html)
        for i in range(0, len(parser.posts)):
            parsed = parser.posts[i]
            actual = self.posts[i]
            self.assertEqual(parsed[0], actual[0])
            self.assertEqual(parsed[1], actual[1])


class RedditPostTest(unittest.TestCase):
    posts = []
