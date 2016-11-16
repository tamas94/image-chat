import ImageAssembler
import ImageSplitter
import MessageEncryption
import MessageDecryption

import cv2
import numpy as np


def test():
    image = cv2.imread("/home/czimbortibor/inputImage.jpg")
    image = cv2.resize(image, (800, 600))
    cv2.imshow("window", image)

    height, width, channels = image.shape
    """ how many parts should there be """
    nrOfParts = 4
    """ how to divide the image into the required number of parts within in a square format """
    nrOfSquares = nrOfParts // 2
    imgPartHeight = height // nrOfSquares
    imgPartWidth = width // nrOfSquares

    images = []
    for i in range(0, width // imgPartWidth):
        for j in range(0, height // imgPartHeight):
            """ 1/nrOfParts part of the original image """
            newImage = image[j * imgPartHeight: j * imgPartHeight + imgPartHeight, i * imgPartWidth: i * imgPartWidth \
                                                                                                     + imgPartWidth]
            images.append(newImage)

    for i in range(0, len(images)):
        cv2.imshow("window" + str(i), images[i])

    cv2.waitKey(0)


test()
