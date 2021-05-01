from abc import ABCMeta, abstractmethod
from slugify import slugify


class Export(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, data: dict):
        raise NotImplementedError('Base method should be implemented')

    def get_slug(self, question: str):
        long = question.partition('?')
        short = slugify(long[0], lowercase=False)
        return short
