from gql import gql, Client
from lime_comb.config import config
from gql.transport.requests import RequestsHTTPTransport


sample_transport = RequestsHTTPTransport(
    url=config.api_url,
    use_json=True,
    headers={"Content-type": "application/json",},
    verify=False,
)

client = Client(
    retries=3, transport=sample_transport, fetch_schema_from_transport=True,
)

get_gpg_query = """query {
  keys(email: "%s") {
    email
    keys {
      data
      id
    }
  }
}
"""

create_gpg_query = """mutation {
  put%sKey(key: {data: "%s", id: "%s", email: "%s", password: "%s"})
  {
    id
    data
    email
  }
}
"""


def get_gpgs(cred, email, key_type="pub"):
    query = get_gpg_query % email
    document = client.execute(gql(query))
    return document["keys"]["keys"]


def delete_gpg(*args, **kwargs):
    pass


def put_gpg(cred, email, data, key_name, key_type="pub", password=""):
    query = create_gpg_query % (
        key_type.capitalize(),
        data.encode("utf-8"),
        key_name,
        email,
        password,
    )
    return client.execute(gql(query))
