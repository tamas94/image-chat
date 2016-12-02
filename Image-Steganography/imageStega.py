import ImageAssembler
import ImageSplitter
import cv2


def test():
    image = cv2.imread("/path/to/image")
    image = cv2.resize(image, (800, 600))
    cv2.imshow("original", image)


    nrOfParts = 4
    imageSplitter = ImageSplitter.ImageSplitter(image, nrOfParts)
    parts = imageSplitter.getParts()

    imageAssembler = ImageAssembler.ImageAssembler(parts)
    fullImage = imageAssembler.getImage()
    cv2.imshow("reconstructed", fullImage)
    cv2.waitKey(0)
    '''
    message = "Hello world!"
    messageEncryptor = MessageEncryption.MessageEncryption(message, image)
    '''
test()
