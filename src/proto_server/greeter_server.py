# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
"""The Python implementation of the GRPC helloworld.Greeter server."""
from concurrent import futures
import logging
import grpc

import proto.v1.helloworld_pb2 as helloworld_pb2
import proto.v1.helloworld_pb2_grpc as helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print('Request from client with name {}'.format(request.name))
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    print('Running gRCP server')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
