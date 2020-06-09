"""Helper functions shared by stubs

Attributes:
    helpers.get_input (func): Function to request user input with a message
    helpers.create_secured_client_channel (func): Create a secured channel with ssl credentials
"""
from contextlib import _GeneratorContextManager
import contextlib
import grpc
from config.credentials import ROOT_CERTIFICATE


def get_input(message: str) -> str:
    """
    Get user input, method made to be mocked in tests

    :param message: To show when input is requested
    :return: Input casted to int
    """
    return input(message)


@contextlib.contextmanager
def create_secured_client_channel(addr: str) -> _GeneratorContextManager:
    """
    Create a secured client channel using the SSL ROOT_CERTIFICATE

    The function return a GeneratorContextManager.
    When called with the `with` statement it will return a grpc._channel.Channel object

    Example:
        $ with create_secured_client_channel('localhost:50500') as _channel:
        $   ...

    :param addr: Channel address
    :return:
    """
    # Channel credential will be valid for the entire channel
    channel_credential = grpc.ssl_channel_credentials(ROOT_CERTIFICATE)
    channel = grpc.secure_channel(addr, channel_credential)
    yield channel
