import abc


class Command(metaclass=abc.ABCMeta):
    def __call__(self, msgs, recipients):
        raise NotImplementedError
