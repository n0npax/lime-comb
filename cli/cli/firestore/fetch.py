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

from cli.auth import get_anon_cred, get_cred

CONF = "/home/n0npax/workspace/lime-comb/cli/client-lime-comb.json"

# cred = get_cred(CONF)
cred = get_anon_cred()


http_request = google.auth.transport.requests.Request()
channel = google.auth.transport.grpc.secure_authorized_channel(
    cred, http_request, "firestore.googleapis.com:443"
)

stub = firestore_pb2_grpc.FirestoreStub(channel)

now = time.time()
seconds = int(now)
timestamp = timestamp_pb2.Timestamp(seconds=seconds)

field_paths = {}


mask = common_pb2.DocumentMask(field_paths=["*"])
# mask = None


project_id = "lime-comb"
database_id = "(default)"
document_path = "free/marcin.niemira@gmail.com"
name = f"projects/{project_id}/databases/{database_id}/documents/{document_path}"

get_document_request = firestore_pb2.GetDocumentRequest(name=name, mask=mask)
get_document_response = stub.GetDocument(get_document_request)

print(get_document_response)

print(dir(get_document_response))
