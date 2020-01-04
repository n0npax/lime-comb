import firebase_admin
import google
from google.auth.transport.requests import AuthorizedSession
from google.cloud import firestore

from auth import get_cred

CONF = "/home/n0npax/workspace/lime-comb/cli/client-lime-comb.json"

cred = get_cred(CONF)
token = cred._refresh_token

db = firestore.Client(credentials=cred, project="lime-comb")

doc_ref = db.collection(u"free").document("foo@foo.foo")
doc_ref.set({u"gpg": u"pppppppppppp"})

# Then query for documents
users_ref = db.collection(u"free")

for doc in users_ref.stream():
    print(u"{} => {}".format(doc.id, doc.to_dict()))
