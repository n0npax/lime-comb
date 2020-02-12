import abc

from cli.firestore.fetch import get_gpgs
from cli.gpg import import_pub_key


class Command(metaclass=abc.ABCMeta):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def _import_keys(self, email, cred, *, key_type="pub"):
        for key_str in get_gpgs(cred, email, key_type=key_type):
            import_pub_key(key_str)
