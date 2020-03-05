import pulumi
from pulumi_gcp import kms, storage, cloudbuild

# Create a KMS KeyRing and CryptoKey to use with the Bucket
keyRing = kms.KeyRing("ci-keyring", location="global")
cryptoKey = kms.CryptoKey("ci-cryptokey", key_ring=keyRing.self_link)

# https://www.pulumi.com/docs/reference/pkg/python/pulumi_gcp/cloudbuild/
_github={"name": "lime-comb", "owner": "n0npax", "push": {"branch": "^master$"}}
_substitutions={}
cb_core = cloudbuild.Trigger(
    "core",
    description="core database",
    filename="core/cloudbuild.yaml",
    github=_github,
    included_files=["core/**"],
    substitutions=_substitutions
)
cb_cli = cloudbuild.Trigger(
    "cli",
    description="cli",
    filename="cli/cloudbuild.yaml",
    github=_github,
    included_files=["cli/**"],
    substitutions=_substitutions
)
cb_cli = cloudbuild.Trigger(
    "web",
    description="web",
    filename="web/cloudbuild.yaml",
    github=_github,
    included_files=["web/**"],
    substitutions=_substitutions
)
infra_cli = cloudbuild.Trigger(
    "infra",
    description="infra",
    filename="infra/cloudbuild.yaml",
    github=_github,
    included_files=["infra/**"],
    substitutions=_substitutions
)