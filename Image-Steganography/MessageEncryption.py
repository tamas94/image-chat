from IMessageMorphing import IMessageMorphing
import numpy as np
import cv2
import imghdr


class MessageEncryption(IMessageMorphing):
    def __init__(self, message, image, fileName):
        super().__init__()
        self.message = message
        self.image = image
        self.fileName = fileName

        self.messageOperation()

    def messageOperation(self):
        imageSize = np.size(self.image) // 8
        print("image size:", imageSize, "bytes")
        textSize = len(self.message)
        print("message size:", textSize, "bytes")

        if textSize > imageSize:
            print("message does not fit in the image!")
            exit()

        """ determine the image format """
        imageType = imghdr.what(self.fileName)
        if imageType == "bmp" or imageType == "png" or imageType == "tiff":
            self.image = self.LSB()
        else:
            if imageType == "jpeg" or imageType == "gif":
                # TODO: implement the encryption for the lossy image formats
                self.image = None

    def LSB(self):
        """ Least Significant Bit method for lossless image formats (e.g. BMP, PNG) """
        message = self.message
        image = self.image

        binaryMsg = self.toBin(message)
        # print(binaryMsg)

        nextChar = binaryMsg.pop(0)
        imgWidth, imgHeight, imgChannels = image.shape
        for row in range(0, imgWidth):
            for col in range(0, imgHeight):
                """ if there are characters left in the message """
                if len(binaryMsg) > 0:
                    """ iterate through the image channels """
                    for channel in range(0, imgChannels):
                        """ if there are bits left in the character's binary representation """
                        if len(nextChar) > 0:
                            """ next bit from the character """
                            nextChar, bitFromMsg = self.nextBit(nextChar)
                            """ image's old pixel """
                            imgPix = image.item(row, col, channel)
                            newBit = imgPix | int(bitFromMsg)
                            """ set the pixel's bit """
                            image.itemset((row, col, channel), newBit)
                        else:
                            """ get the new character from the message """
                            nextChar = binaryMsg.pop(0)
                else:
                    return image

    def nextBit(self, binValue):
        if binValue is not None:
            n = len(binValue)
            if n > 0:
                return binValue[:n-1], binValue[n-1]
        return None, None

    def toBin(self, text):
        """ converts the text into binary format """
        bytesA = bytearray(text, "utf-8")
        """ into a byte array, ie: [72, 101, 108, 108, 111, 32, 119, 111] """
        # print(list(bytesA))
        binF = list(map(bin, bytesA))
        """ every element into its binary format, ie: ['0b1001000', '0b1100101', '0b1101100'] """
        # print(binF)
        """ remove the first 2 characters from every element in the array, ie: ['1001000', '1100101', '1101100'] """
        binFormat = list(map(lambda strA: strA[2:], binF))  # [2:] -> slice syntax, everything starting from the 2nd index
        res = list(map(self.completeBinary, binFormat))
        return res

    """ if the binary representation is not 8 bits long """
    def completeBinary(self, binStr):
        n = len(binStr)
        m = 8 - n
        return ("0" * m) + binStr

    def getImage(self):
        return self.image
