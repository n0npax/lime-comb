import abc
from cli.gpg import import_pub_key
from cli.firestore.fetch import get_gpg

class Command(metaclass=abc.ABCMeta):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def _import_key(self, email, cred):
        key_str = get_gpg(cred, email)
        import_pub_key(key_str)