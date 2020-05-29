"""
Config variables for the gRPC server and clients/stubs

Attributes:
    config.GRPC_SERVER_PORT (int): Port used to run the gRPC server and invoke the stubs
"""
import os

GRPC_SERVER_PORT = int(os.environ.get('GRPC_SERVER_PORT', 50051))
