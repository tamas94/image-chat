import IMessageMorphing


class MessageDecryption(IMessageMorphing.IMessageMorphing):
    def __init__(self, image, messageLen, fileName):
        super().__init__()
        self.image = image
        self.messageLen = messageLen
        self.fileName = fileName

        self.bytess = []
        self.message = self.messageOperation()
        # print(self.bytess)

    def messageOperation(self):
        image = self.image
        messageLen = self.messageLen

        message = ""
        imgWidth, imgHeight, imgChannels = image.shape
        k = 0
        binaryStr = []
        counter = 0

        for row in range(0, imgWidth):
            for col in range(0, imgHeight):
                for channel in range(0, imgChannels):
                    imgPix = image.item(row, col, channel)
                    """ first bit of the pixel """
                    imgBit = imgPix & 1
                    binaryStr.insert(0, imgBit)
                    k += 1
                    if k > 8:
                        counter += 1
                        resInt = self.binToInt(binaryStr)
                        message += chr(resInt)
                        k = 0
                        binaryStr = []
                    if counter == messageLen:
                        return message

        return ""

    def binToInt(self, binList):
        binStr = "".join(str(i) for i in binList)
        self.bytess.append(binStr)
        res = int(binStr, 2)
        return res

    def getMessage(self):
        return self.message
