import abc


class Command(metaclass=abc.ABCMeta):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
