from ImageProcessorFactory import *

#Base class for Image Processing
class ImageProcessCommand:
    
    def __init__(self, operation_):
        self.operation = operation_

    def execute(self, img):
        pass

#Command class to flip image
class FlipCommand(ImageProcessCommand):
    
    def execute(self, img):
        flip = self.operation.process(img)
        return flip

#Command class to create grayscale image
class GrayScaleCommand(ImageProcessCommand):
    
    def execute(self, img):
        gray = self.operation.process(img)
        return gray

#Command class to rotate image
class RotateCommand(ImageProcessCommand):
    
    def execute(self, img):
        rotate = self.operation.process(img)
        return rotate

#Command class to resize image
class ResizeCommand(ImageProcessCommand):
    
    def execute(self, img):
        resize = self.operation.process(img)
        return resize

#Command class to create thumbnail of the image
class ThumbnailCommand(ImageProcessCommand):
    
    def execute(self, img):
        thumbnail = self.operation.process(img)
        return thumbnail