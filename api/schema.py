import graphene

from database import list_gpg_ids
import database


class GpgKey(graphene.Interface):
    id = graphene.ID()
    email = graphene.String()
    data = graphene.String()


class PubKey(graphene.ObjectType):
    class Meta:
        interfaces = (GpgKey,)


class PrivKey(graphene.ObjectType):
    class Meta:
        interfaces = (GpgKey,)

    password = graphene.String()


class GpgKeys(graphene.ObjectType):
    class Meta:
        description = "gpg key id"

    email = graphene.String()
    keys = graphene.List(lambda: PubKey)

    def resolve_keys(self, info):
        pub_keys = []
        for document in database.get_gpgs(self.email):
            pub_keys.append(PubKey(**document))
        print(pub_keys[0], type(pub_keys[0]))
        return pub_keys


class Query(graphene.ObjectType):
    keys = graphene.Field(GpgKeys, email=graphene.String())
    pub_key = graphene.Field(PubKey, email=graphene.String(), id=graphene.String())
    priv_key = graphene.Field(PrivKey, email=graphene.String(), id=graphene.String())

    def resolve_keys(self, info, email):
        return GpgKeys(email=email)

    def resolve_pub_key(self, info, email, id):
        document = database.get_gpg(email, id)
        return PubKey(**document)

    def resolve_priv_key(self, info, email, id):
        document = database.get_gpg(email, id, key_type="priv")
        return PrivKey(**document)
