import IImageMorphing
import cv2
import numpy as np


class ImageSplitter(IImageMorphing.IImageMorphing):
    def __init__(self, image, nrOfParts):
        super().__init__()
        self.image = image
        self.nrOfParts = nrOfParts
        self.parts = []

        self.imageOperation()

    def imageOperation(self):
        height, width, channels = self.image.shape
        """ how to divide the image into the required number of parts within a square format """
        nrOfSquares = self.nrOfParts // 2
        imgPartHeight = height // nrOfSquares
        imgPartWidth = width // nrOfSquares

        k = 1
        for i in range(0, width // imgPartWidth):
            for j in range(0, height // imgPartHeight):
                """ 1/nrOfParts part of the original image """
                newImgPart = self.image[j * imgPartHeight: j * imgPartHeight + imgPartHeight,
                             i * imgPartWidth: i * imgPartWidth + imgPartWidth]

                """ set the first Green pixel to the image part's order """
                newImgPart.itemset((0, 0, 1), k)
                self.parts.append(newImgPart)
                k += 1

    def getParts(self):
        return self.parts
