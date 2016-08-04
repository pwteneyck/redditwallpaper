# determines the best way to crop a given picture to (hopefully) cut out as
# little of the good stuff as possible

import ctypes
import PIL
import logging

class ImageAnalyzer:
    screenWidth = 0
    screenHeight = 0
    image = None
    logger = logging.getLogger('redditdesktop.imageanalyzer')

    def __init__(self, i):
        self.image = i
        u = ctypes.windll.user32
        self.screenWidth = u.GetSystemMetrics(0)
        self.screenHeight = u.GetSystemMetrics(1)
        self.resizeForScreen()

    def resizeForScreen(self):
        # w/h is too high :: image is too wide, so we scale height to screenHeight
        screenRatio = self.screenWidth / self.screenHeight
        imageRatio = self.image.width / self.image.height
        if imageRatio > screenRatio:
            resizeRatio = self.screenHeight / self.image.height
            self.image = self.image.resize((int(self.image.width*resizeRatio), self.screenHeight), PIL.Image.ANTIALIAS)
        else:
            resizeRatio = self.screenWidth / self.image.width
            self.image = self.image.resize((self.screenWidth, int(self.image.height*resizeRatio)), PIL.Image.ANTIALIAS)

    def getCropAreas(self):
        if self.image.width != self.screenWidth:
            dif = self.image.width - self.screenWidth
            if dif < 1:
                print('ERROR:: image not resized correctly - ' + str(self.image.width) + 'x' + str(self.image.height))
                self.logger.error('image not resized correctly - ' + str(self.image.width) + 'x' + str(self.image.height))
            return ((0, 0, dif, self.image.height), (self.screenWidth, 0, self.image.width, self.image.height))
        elif self.image.height != self.screenHeight:
            dif = self.image.height - self.screenHeight
            if dif < 1:
                print('ERROR:: image not resized correctly - ' + str(self.image.width) + 'x' + str(self.image.height))
                self.logger.error('image not resized correctly - ' + str(self.image.width) + 'x' + str(self.image.height))
            return ((0, 0, self.image.width, dif), (0, self.screenHeight, self.image.width, self.image.height))

    # precondition: resizeForScreen has already been called
    def cropToScreenRatio(self):
        if self.image.width > self.screenWidth:
            cut = int((self.image.width - self.screenWidth) / 2)
            self.image = self.image.crop((cut, 0, self.image.width - cut, self.image.height))
        elif self.image.height > self.screenHeight:
            cut = int((self.image.height - self.screenHeight) / 2)
            self.image = self.image.crop((0, cut, self.image.width, self.image.height - cut))
