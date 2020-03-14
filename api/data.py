pub_keys_data = {}
priv_keys_data = {}


def setup():
    from schema import PubKey, PrivKey

    global pub_keys_data, priv_keys_data
    pub0 = PubKey(id="1000", email="example@example.com")
    pub1 = PubKey(id="1001", email="example@example.com")
    pub3 = PubKey(id="1002", email="example2@example.com")

    pub_keys_data = {
        "1000": pub0,
        "1001": pub1,
        "1002": pub3,
    }

    priv1 = PrivKey(id="2000", email="example@example.com", password="aaa",)
    priv2 = PrivKey(id="2001", email="example2@example.com", password="aaa",)

    priv_keys_data = {"2000": priv1, "2001": priv2}


def get_character(id):
    return pub_keys_data.get(id) or priv_keys_data.get(id)


def get_keys(email):
    if email == "marcin@niemira.net":
        return pub_keys_data.get("1000")
    return priv_keys_data.get("2001")


def get_pub_key(id):
    return pub_keys_data.get(id)


def get_priv_key(id):
    return priv_keys_data.get(id)
