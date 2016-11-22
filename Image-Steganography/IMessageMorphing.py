from abc import ABCMeta, abstractmethod


class IMessageMorphing(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def messageOperation(self):
        raise NotImplementedError
