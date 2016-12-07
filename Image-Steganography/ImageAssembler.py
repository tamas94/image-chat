import math

import numpy as np

import IImageMorphing


class ImageAssembler(IImageMorphing.IImageMorphing):
    def __init__(self, parts):
        super().__init__()
        self.parts = parts
        """ size of the 2 dimensional array which will contain all of the image parts """
        self.sizeOfM = int(round(math.sqrt(len(parts)), 1))
        self.fullImage = []

        self.imageOperation()

    def imageOperation(self):
        partsM = []
        for i in range(0, self.sizeOfM):
            partsM.append([])
            for j in range(0, self.sizeOfM):
                partsM[i].append(self.parts[i * self.sizeOfM + j])

        """ stitch together the first row """
        self.fullImage = partsM[0][0]
        for i in range(1, self.sizeOfM):
            self.fullImage = np.concatenate((self.fullImage, partsM[0][1]), axis=1)

        """ stitch the rows starting from the 2nd one """
        for i in range(1, self.sizeOfM):
            imageRow = partsM[i][0]
            for j in range(1, self.sizeOfM):
                imageRow = np.concatenate((imageRow, partsM[i][j]), axis=1)
            """ after a row is completed attach it below the previously stitched together rows """
            self.fullImage = np.concatenate((self.fullImage, imageRow), axis=0)

    def getImage(self):
        return self.fullImage
