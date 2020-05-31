"""
Config variables for the gRPC server and clients/stubs

Attributes:
    config.GRPC_SERVER_PORT (int): Port used to run the gRPC server and invoke the stubs
    config.MAX_PAGE_SIZE (int): Define the max number of items per page when listing resources.
"""
import os

GRPC_SERVER_PORT = int(os.environ.get('GRPC_SERVER_PORT', 50051))
MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', 50))
