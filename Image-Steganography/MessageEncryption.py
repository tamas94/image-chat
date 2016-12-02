import IMessageMorphing
import numpy as np


class MessageEncryption(IMessageMorphing.IMessageMorphing):
    def __init__(self, message, image):
        super().__init__()
        self.message = message
        self.image = image

        self.messageOperation()

    def messageOperation(self):
        imageSize = np.size(self.image) // 8
        print("image size:", imageSize, "bytes")
        textSize = len(self.message)
        print("message size:", textSize, "bytes")

        if textSize > imageSize:
            print("message does not fit in the image!")
            exit()

        self.LSB()

    def LSB(self):
        pass
