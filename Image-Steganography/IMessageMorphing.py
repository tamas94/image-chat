from abc import ABCMeta, abstractmethod
import numpy
import cv2


class IMessageMorphing(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def messageOperation(self):
        raise NotImplementedError
