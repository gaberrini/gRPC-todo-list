"""Helper functions shared by stubs

Attributes:
    helpers.get_input (func): Function to request user input with a message
    helpers.create_secured_client_channel (func): Create a secured channel with ssl credentials
"""
import contextlib
import grpc
from grpc._channel import Channel
from config.credentials import ROOT_CERTIFICATE


def get_input(message: str) -> str:
    """
    Get user input, method made to be mocked in tests

    :param message: To show when input is requested
    :return: Input casted to int
    """
    return input(message)


@contextlib.contextmanager
def create_secured_client_channel(addr: str) -> Channel:
    """
    Create a secured client channel using the SSL ROOT_CERTIFICATE
    and yield it to be used in a `with` statement

    :param addr: Channel address
    :return:
    """
    # Channel credential will be valid for the entire channel
    channel_credential = grpc.ssl_channel_credentials(ROOT_CERTIFICATE)
    channel = grpc.secure_channel(addr, channel_credential)
    yield channel
