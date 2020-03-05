import pulumi
from pulumi_gcp import cloudbuild, kms, storage

# Create a KMS KeyRing and CryptoKey to use with the Bucket
keyRing = kms.KeyRing("ci-keyring", location="global")
cryptoKey = kms.CryptoKey("ci-cryptokey", key_ring=keyRing.self_link)

# https://www.pulumi.com/docs/reference/pkg/python/pulumi_gcp/cloudbuild/
_github = {"name": "lime-comb", "owner": "n0npax", "push": {"branch": "^master$"}}
_substitutions = {}
cloudbuilds = {}
for component in ("core", "infra", "web", "cli", "lambda"):
    cloudbuilds[component] = cloudbuild.Trigger(
        component,
        description=component,
        filename=f"{component}/cloudbuild.yaml",
        github=_github,
        included_files=[f"{component}/**"],
        substitutions=_substitutions,
    )