import base64

import google.auth.transport.grpc
import google.auth.transport.requests
from google.cloud import firestore


from cli.config import Config
from cli.logger.logger import logger


def doc_path(*, email, key_type, key_name):
    _, domain = email.split("@")

    return f"{domain}", f"{email}/{key_name}/{key_type}"


def get_gpg(cred, email, key_name, *, key_type="pub"):
    db = firestore.Client(credentials=cred, project=Config.app_name)
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)

    pub_key = db.collection(collection_id).document(name)

    return pub_key["data"].string_value


def get_gpgs(cred, email, *, key_type="pub"):
    for key_name in list_gpg_ids(cred, email, key_type=key_type):
        yield get_gpg(cred, email, key_type=key_type, key_name=key_name)


def put_gpg(cred, email, data, key_name, *, key_type="pub"):
    db = firestore.Client(credentials=cred, project=Config.app_name)
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    pub_key = db.collection(collection_id).document(name)
    pub_key.set({"data": data})


def list_gpg_ids(cred, email, key_type="pub"):
    db = firestore.Client(credentials=cred, project=Config.app_name)
    collection_id, _ = doc_path(email=email, key_type=key_type, key_name=key_name)

    return db.collection(collection_id).list_documents()


def _decode_base64(s):
    return base64.b64decode(s).decode("utf-8")


def _encode_base64(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")
