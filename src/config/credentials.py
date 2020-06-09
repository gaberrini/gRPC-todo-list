"""Loading SSL credentials for gRPC Server and Stubs.

Attributes:
    SERVER_CERTIFICATE (bytes): Server cert
    SERVER_CERTIFICATE_KEY (bytes): Server cert key
    ROOT_CERTIFICATE (bytes): Client cert, used by the stubs
    credentials._load_credential_from_file (func): Load credentials from files
"""
import os


def _load_credential_from_file(filepath: str) -> bytes:
    """
    Read a credential file from file.

    :param filepath:
    :return: Cert file
    """
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, 'rb') as f:
        return f.read()


SERVER_CERTIFICATE = _load_credential_from_file('credentials/localhost.crt')
SERVER_CERTIFICATE_KEY = _load_credential_from_file('credentials/localhost.key')
ROOT_CERTIFICATE = _load_credential_from_file('credentials/root.crt')
