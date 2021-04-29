from abc import ABCMeta, abstractmethod


class Export(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError('Base method should be implemented')
