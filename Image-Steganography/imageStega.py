import argparse
import os

import cv2

from MessageDecryption import MessageDecryption
from MessageEncryption import MessageEncryption


class OpenCVException(Exception):
    pass


def main():
    args = parseArguments()
    message = args.message
    fileName = args.fileName
    nrOfParts = args.nrOfParts

    if args.fileName is None:
        dirPath = os.getcwd()
        fileName = os.path.join(dirPath, "images", "inputImage.png")
    image = cv2.imread(fileName)
    if image is not None:
        image = cv2.resize(image, (800, 600))
        #cv2.imshow("original", image)
    else:
        raise OpenCVException("Not a valid image file!")

    '''
    imageSplitter = ImageSplitter(image, nrOfParts)
    parts = imageSplitter.getParts()

    imageAssembler = ImageAssembler(parts)
    fullImage = imageAssembler.getImage()
    cv2.imshow("reconstructed", fullImage)
    cv2.waitKey(0)
    '''

    message = "Hello world! This should be encrypted and you shouldn't see this."
    print("original message: ", message)
    messageEncryptor = MessageEncryption(message, image, fileName)
    stegaImage = messageEncryptor.getImage()
    # cv2.imshow("steganographed image", stegaImage)
    # cv2.waitKey(0)

    messageLen = len(message)
    if stegaImage is not None:
        messageDecryptor = MessageDecryption(stegaImage, messageLen, fileName)
        decryptedMessage = messageDecryptor.getMessage()
        print("decrypted message: ", decryptedMessage)
    else:
        raise NotImplementedError


def parseArguments():
    parser = argparse.ArgumentParser(description="Image steganography. Supply a text and an image and then the script "
                                                 "will hide the text inside the image")
    parser.add_argument("-t", "--text", help="the input text", dest="message", default="Hello")
    parser.add_argument("-i", "--img", help="the input image", dest="fileName")
    parser.add_argument("-nr", "--nr-of-parts", help="to how many parts should the script split the result image",
                        dest="nrOfParts", default=4)
    return parser.parse_args()


if __name__ == "__main__":
    main()
