import base64
import json
import os
import subprocess
import sys
import time

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
from google.cloud.firestore_v1.proto import (common_pb2, common_pb2_grpc,
                                             document_pb2, document_pb2_grpc,
                                             firestore_pb2, firestore_pb2_grpc,
                                             write_pb2, write_pb2_grpc)
from google.cloud.firestore_v1.types import Document, Value
from google.oauth2 import service_account
from google.protobuf import empty_pb2, timestamp_pb2

import grpc
from cli.auth.google import get_anon_cred, get_cred
from cli.config import Config
from cli.logger.logger import logger


def doc_path(email, key_type="pub", key_name="default"):
    logger.info(f"fetching gpg for {email}")
    project_id = "lime-comb"  # TODO from config
    database_id = "(default)"
    _, domain = email.split("@")
    document_path = doc_path_e(domain, email, key_type, key_name)
    name = f"projects/{project_id}/databases/{database_id}/documents/{document_path}"
    return name


def doc_path_e(domain, email, key_type, key_name):
    return f"{domain}/{email}/{key_type}/{key_name}"


def get_gpg(cred, email, key_type="pub", key_name="default"):
    name = doc_path(email, key_type, key_name)
    mask = common_pb2.DocumentMask(field_paths=["data"])
    pub_key = get_document(cred, name, mask)
    return _decode_base64(pub_key["data"].string_value)


def put_gpg(cred, email, data, key_type="pub", key_name="default"):
    document = Document(fields={"data": Value(string_value=data)})
    name = doc_path(email, key_type, key_name)
    mask = common_pb2.DocumentMask(field_paths=["data"])
    parent, _, collection_id = name.rsplit("/", 2)
    return put_document(
        cred, parent, collection_id, document=document, document_id=key_type, mask=mask
    )


def get_document(cred, name, mask=None):
    channel = _create_channel(cred)
    stub = firestore_pb2_grpc.FirestoreStub(channel)

    get_document_request = firestore_pb2.GetDocumentRequest(name=name, mask=mask)
    get_document_response = stub.GetDocument(get_document_request)
    return get_document_response.fields


def put_document(cred, parent, collection_id, document, document_id=None, mask=None):
    channel = _create_channel(cred)
    stub = firestore_pb2_grpc.FirestoreStub(channel)

    put_document_request = firestore_pb2.CreateDocumentRequest(
        parent=parent,
        document_id=document_id,
        document=document,
        collection_id=collection_id,
    )
    put_document_response = stub.CreateDocument(put_document_request)
    return put_document_response.fields


def delete_document(cred, doc_name):
    channel = _create_channel(cred)
    stub = firestore_pb2_grpc.FirestoreStub(channel)
    delete_document_request = firestore_pb2.DeleteDocumentRequest(name=doc_name)
    stub.DeleteDocument(delete_document_request)


def _create_channel(cred):
    http_request = google.auth.transport.requests.Request()
    channel = google.auth.transport.grpc.secure_authorized_channel(
        cred, http_request, Config.firestore_target
    )
    return channel


def _decode_base64(s):
    return base64.b64decode(s).decode("utf-8")


def _encode_base64(s):
    return base64.b64encode(s)
