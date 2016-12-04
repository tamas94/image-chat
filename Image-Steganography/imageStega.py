from ImageAssembler import ImageAssembler
from ImageSplitter import ImageSplitter
from MessageEncryption import MessageEncryption
from MessageDecryption import MessageDecryption
import cv2


def test():
    image = cv2.imread("path/to/image")
    image = cv2.resize(image, (800, 600))
    cv2.imshow("original", image)

    '''
    nrOfParts = 4
    imageSplitter = ImageSplitter(image, nrOfParts)
    parts = imageSplitter.getParts()

    imageAssembler = ImageAssembler(parts)
    fullImage = imageAssembler.getImage()
    cv2.imshow("reconstructed", fullImage)
    cv2.waitKey(0)
    '''

    message = "Hello world! This should be encrypted and you shouldn't see this."
    print("original message: ", message)
    messageEncryptor = MessageEncryption(message, image)
    stegaImage = messageEncryptor.getImage()
    cv2.imshow("steganographed image", stegaImage)
    cv2.waitKey(0)

    messageLen = len(message)
    messageDecryptor = MessageDecryption(stegaImage, messageLen)
    decryptedMessage = messageDecryptor.getMessage()
    print("decrypted message: ", decryptedMessage)

test()
