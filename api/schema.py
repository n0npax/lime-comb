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
        # TODO lazyloading for not id fields?
        pub_keys = []
        for document in database.get_gpgs(self.email):
            pub_keys.append(PubKey(**document))
        return pub_keys


class Query(graphene.ObjectType):
    keys = graphene.Field(GpgKeys, email=graphene.String(required=True))
    pub_key = graphene.Field(
        PubKey, email=graphene.String(required=True), id=graphene.String(required=True)
    )
    priv_key = graphene.Field(
        PrivKey, email=graphene.String(required=True), id=graphene.String(required=True)
    )

    def resolve_keys(self, info, email):
        return GpgKeys(email=email)

    def resolve_pub_key(self, info, email, id):
        document = database.get_gpg(email, id)
        return PubKey(**document)

    def resolve_priv_key(self, info, email, id):
        document = database.get_gpg(email, id, key_type="priv")
        return PrivKey(**document)


class GpgKeyInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    email = graphene.String()
    data = graphene.String(required=True)
    password = graphene.String()


class IdInput(graphene.InputObjectType):
    id = graphene.ID(required=True)


class PutPubKey(graphene.Mutation):
    class Arguments:
        key = GpgKeyInput(required=True)

    Output = PubKey

    def mutate(root, info, key):
        return PubKey(email=key.email, id=key.id, data=key.data)


class PutPrivKey(graphene.Mutation):
    class Arguments:
        key = GpgKeyInput(required=True)

    Output = PrivKey

    def mutate(root, info, key):
        return PrivKey(email=key.email, id=key.id, data=key.data, password=key.password)


class DeleteKey(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    Output = PubKey

    def mutate(root, info, id):
        return PubKey(id=id)


class Mutation(graphene.ObjectType):
    put_pub_key = PutPubKey.Field()
    put_priv_key = PutPrivKey.Field()
    delete_key = DeleteKey.Field()
