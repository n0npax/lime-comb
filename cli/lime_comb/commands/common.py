from lime_comb.validators.email import lc_validate_email
from lime_comb.validators.file import validate_filepath


def add_message_parameters(parser):
    parser.add_argument(
        "-f",
        "--file",
        dest="files",
        required=False,
        action="append",
        help="file",
        default=[],
        type=validate_filepath,
    )
    parser.add_argument(
        "-m",
        "--message",
        dest="messages",
        required=False,
        action="append",
        help="message",
        default=[],
    )


def add_msg_recv(parser):
    parser.add_argument(
        "-t",
        "--to",
        dest="recipients",
        required=False,
        action="append",
        default=[],
        help="recipient of the message",
        type=lc_validate_email,
    )


def add_msg_merge(parser):
    parser.add_argument(
        "--merge-messages",
        "--mm",
        dest="merge_messages",
        required=False,
        action="store_true",
        default=False,
        help="merge multile messages into 1",
    )
