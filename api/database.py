import base64

from google.cloud import firestore


import logging
import sys

logging.basicConfig(stream=sys.stdout)
app_name = "lime-comb"
logger = logging.getLogger(app_name)


def doc_path(*, email, key_type, key_name):
    _, domain = email.split("@")
    return f"{domain}", f"{email}/{key_name}/{key_type}"


db = firestore.Client(project=app_name)


def get_gpg(email, key_name, *, key_type="pub"):
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    logger.info(
        f"(firebase registry) pull gpgs for {email} as {name} from {collection_id}"
    )
    document = db.collection(collection_id).document(name).get().to_dict()
    if not "data" in document:
        logger.error("Cannot fetch gpg key")
        return None
    document["id"] = key_name
    document["email"] = email
    return document


def get_gpgs(email, *, key_type="pub"):
    for key_name in list_gpg_ids(email, key_type=key_type):
        yield get_gpg(email, key_type=key_type, key_name=key_name)


def put_gpg(email, data, key_name, *, key_type="pub", password=None):
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    logger.info(
        f"(firebase registry) push gpg for {email} as {name} from {collection_id}"
    )
    pub_key = db.collection(collection_id).document(name)
    document = {"data": data}
    if key_type == "priv" and password:
        document["password"] = password
    pub_key.set(document)


def list_gpg_ids(email, key_type="pub"):
    collection_id, _ = doc_path(
        email=email, key_type=key_type, key_name="key_id_placeholder"
    )
    logger.info(
        f"(firebase registry) list gpgs for {email}(just email) from {collection_id}"
    )
    for d in db.collection(collection_id).document(email).collections():
        yield d.id


def delete_gpg(email, key_name, *, key_type="pub"):
    collection_id, name = doc_path(email=email, key_type=key_type, key_name=key_name)
    logger.info(
        f"(firebase registry) rm gpg for {email} as {name} from {collection_id}"
    )
    return db.collection(collection_id).document(name).delete()


def _decode_base64(s):
    return base64.b64decode(s).decode("utf-8")


def _encode_base64(s):
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")
