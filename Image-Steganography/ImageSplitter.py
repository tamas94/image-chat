import IImageMorphing
import cv2
import numpy as np


class ImageSplitter(IImageMorphing.IImageMorphing):
    def __init__(self, image):
        super().__init__()
        self.image = image

    def imageOperation(self):
        newSize = self.image.shape
