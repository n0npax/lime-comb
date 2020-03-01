import base64

from google.cloud import firestore

from lime_comb.config import config
from lime_comb.logger.logger import logger


def doc_path(*, email, key_type, key_name):
    _, domain = email.split("@")
    return f"{domain}", f"{email}/{key_name}/{key_type}"


def get_firestore_db(cred):
    return firestore.Client(credentials=cred, project=config.app_name)


def get_gpg(cred, email, key_name, *, key_type="pub"):
    logger.debug(f"fetching gpg key for: {email} (firebase registry)")
    db = get_firestore_db(cred)
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    key = db.collection(collection_id).document(name).get().to_dict()
    try:
        return key["data"]
    except KeyError:
        return None


def get_gpgs(cred, email, *, key_type="pub"):
    for key_name in list_gpg_ids(cred, email, key_type=key_type):
        yield get_gpg(cred, email, key_type=key_type, key_name=key_name)


def put_gpg(cred, email, data, key_name, *, key_type="pub", password=None):
    logger.debug(f"pushing gpg key for: {email} (firebase registry)")
    db = get_firestore_db(cred)
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    pub_key = db.collection(collection_id).document(name)
    document = {"data": data}
    if key_type == "priv" and password:
        document["password"] = password
    pub_key.set(document)


def list_gpg_ids(cred, email, key_type="pub"):
    db = get_firestore_db(cred)
    collection_id, _ = doc_path(
        email=email, key_type=key_type, key_name="key_id_placeholder"
    )
    for d in db.collection(collection_id).document(email).collections():
        yield d.id


def delete_gpg(cred, email, key_name, *, key_type="pub"):
    logger.debug(f"deleting gpg key for: {email} (firebase registry)")
    db = get_firestore_db(cred)
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    return db.collection(collection_id).document(name).delete()


def _decode_base64(s):
    return base64.b64decode(s).decode("utf-8")


def _encode_base64(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")
