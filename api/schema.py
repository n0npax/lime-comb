import graphene

from data import get_priv_key, get_keys, get_pub_key
import data
from database import list_gpg_ids


class GpgKey(graphene.Interface):
    id = graphene.ID()
    email = graphene.String()


class GpgKeys(graphene.ObjectType):
    class Meta:
        description = "gpg key id"

    id = graphene.ID()
    ids = graphene.List(graphene.String)
    email = graphene.String()


class PubKey(graphene.ObjectType):
    class Meta:
        interfaces = (GpgKey,)


class PrivKey(graphene.ObjectType):
    class Meta:
        interfaces = (GpgKey,)

    password = graphene.String()


class Query(graphene.ObjectType):
    keys = graphene.Field(GpgKeys, email=graphene.String())
    pub_key = graphene.Field(PubKey, id=graphene.String())
    priv_key = graphene.Field(PrivKey, id=graphene.String())

    def resolve_keys(self, info, email):
        keys = []
        for k in list_gpg_ids(email):
            keys.append(k)
        return GpgKeys(ids=keys, email=email)

    def resolve_pub_key(self, info, id):
        return get_pub_key(id)

    def resolve_priv_key(self, info, id):
        return get_priv_key(id)
