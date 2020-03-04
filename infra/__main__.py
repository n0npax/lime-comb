import pulumi
from pulumi_gcp import kms, storage

# Create a KMS KeyRing and CryptoKey to use with the Bucket
keyRing = kms.KeyRing("ci-keyring", location="global")
cryptoKey = kms.CryptoKey("ci-cryptokey", key_ring=keyRing.self_link)
