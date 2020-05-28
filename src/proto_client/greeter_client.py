# Copyright 2015 gRPC authors.
# Licensed under the Apache License, Version 2.0 (the "License");
"""The Python implementation of the GRPC helloworld.Greeter client."""
import logging
import grpc

import proto.v1.helloworld_pb2 as helloworld_pb2
import proto.v1.helloworld_pb2_grpc as helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    name = 'test'
    print('Running gRPC from client with name {}'.format(name))
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=name))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
