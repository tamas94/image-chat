from abc import ABCMeta, abstractmethod


class IImageMorphing(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def imageOperation(self):
        raise NotImplementedError
