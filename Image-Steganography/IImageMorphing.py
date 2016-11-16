from abc import ABCMeta, abstractmethod
import numpy
import cv2


class IImageMorphing(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def imageOperation(self):
        raise NotImplementedError
