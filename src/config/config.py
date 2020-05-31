"""
Config variables for the gRPC server and clients/stubs

Attributes:
    GRPC_SERVER_PORT (int): Port used to run the gRPC server and invoke the stubs
    MAX_PAGE_SIZE (int): Define the max number of items per page when listing resources.
    TESTING_ENVIRONMENT (str): Name of testing environment.
    ENVIRONMENT (str): Define the running environment, if it's `TESTING_ENVIRONMENT` Test DB PATH will be assigned
"""
import os

GRPC_SERVER_PORT = int(os.environ.get('GRPC_SERVER_PORT', 50051))
MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', 50))

TESTING_ENVIRONMENT = 'testing'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
