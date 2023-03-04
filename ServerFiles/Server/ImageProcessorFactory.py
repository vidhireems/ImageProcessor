# import cv2
from PIL import Image

#Base class to create a factory object based on the operation
class ImageProcessFactory:
    @staticmethod
    #Factory method
    def getOperation(op,param=None):
        if op == "gray":
            return GrayScaleOperation()
        elif op == "flip":
            return FlipOperation(param)
        elif op == "rotate":
            return RotateOperation(param)
        elif op == "resize":
            return ResizeOperation(param)
        elif op == "thumbnail":
            return ThumbnailOperation(param)
        else:
            raise NotImplementedError(f"This {op} is not supported")

#Flips the image based
class FlipOperation:
    def __init__(self, isHorizontal):
        self.isHorizontal_ = isHorizontal
    def process(self, img):
        if self.isHorizontal_:
            flip = img.transpose(Image.FLIP_LEFT_RIGHT)
            return flip
        elif not self.isHorizontal_:
            flip = img.transpose(Image.FLIP_TOP_BOTTOM)
            return flip

#Converts the image to grayscale
class GrayScaleOperation:
    def process(self, img):
        gray = img.convert('L')
        return gray

#Rotates the image
class RotateOperation:
    def __init__(self, angle):
        self.angle_ = angle
    def process(self, img): 
        rotate = img.rotate(self.angle_,expand=True)
        return rotate

#Resizes the image
class ResizeOperation:
    def __init__(self, size):
        self.size_ = size
    def process(self, img):
        resize = img.resize(self.size_)
        return resize

#Generates the thumbnail of the image
class ThumbnailOperation:
    def __init__(self, size):
        self.size_ = size
    def process(self, img):
        imageCopy = img.copy()
        imageCopy.thumbnail(self.size_)
        return imageCopy