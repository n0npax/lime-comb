import base64
import json
import os
import subprocess
import sys
import time

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import grpc
from google.cloud.firestore_v1.proto import (common_pb2, common_pb2_grpc,
                                             document_pb2, document_pb2_grpc,
                                             firestore_pb2, firestore_pb2_grpc,
                                             write_pb2, write_pb2_grpc)
from google.oauth2 import service_account
from google.protobuf import empty_pb2, timestamp_pb2

from cli.auth.google import get_anon_cred, get_cred
from cli.logger.logger import logger


def get_gpg(cred, email):
    logger.info(f"fetching gpg for {email}")
    project_id = "lime-comb"  # TODO from config
    database_id = "(default)"
    _, domain = email.split("@")
    document_path = f"{domain}/{email}/pub/default"
    name = f"projects/{project_id}/databases/{database_id}/documents/{document_path}"
    mask = common_pb2.DocumentMask(field_paths=["data"])
    pub_key = get_document(cred, name, mask)
    return _decode_base64(pub_key["data"].string_value)


def get_document(cred, name, mask=None):
    http_request = google.auth.transport.requests.Request()
    channel = google.auth.transport.grpc.secure_authorized_channel(
        cred, http_request, "firestore.googleapis.com:443"
    )
    stub = firestore_pb2_grpc.FirestoreStub(channel)

    get_document_request = firestore_pb2.GetDocumentRequest(name=name, mask=mask)
    get_document_response = stub.GetDocument(get_document_request)
    return get_document_response.fields


def _decode_base64(s):
    return base64.b64decode(s).decode("utf-8")
