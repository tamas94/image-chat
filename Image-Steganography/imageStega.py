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

    nrOfParts = 4
    imageSplitter = ImageSplitter.ImageSplitter(image, nrOfParts)
    parts = imageSplitter.getParts()
    for i in range(0, len(parts)):
        cv2.imshow("part " + str(i+1), parts[i])

    cv2.waitKey(0)

test()
