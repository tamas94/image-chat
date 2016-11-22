import cv2

import ImageAssembler
import ImageSplitter


def test():
    image = cv2.imread("/home/czimbortibor/inputImage.jpg")
    image = cv2.resize(image, (800, 600))
    cv2.imshow("original", image)

    nrOfParts = 4
    imageSplitter = ImageSplitter.ImageSplitter(image, nrOfParts)
    parts = imageSplitter.getParts()
    # for i in range(0, len(parts)):
    #   cv2.imshow("part " + str(i+1), parts[i])
    imageAssembler = ImageAssembler.ImageAssembler(parts)
    fullImage = imageAssembler.getImage()
    cv2.imshow("reconstructed", fullImage)
    cv2.waitKey(0)

test()
