"""The Python implementation of the GRPC todolists.TodoLists client."""
import grpc
import os
import sys
from typing import Optional
from grpc._channel import _InactiveRpcError
from grpc import StatusCode

# Not good practice, add src to python path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


def create_list(name: str) -> Optional[todolists_pb2.CreateListReply]:
    """
    Call to the TodoLists.Create gRPC with the defined name

    :param name: name for the new list
    :return:
    """
    print('Calling TodoLists.Create with name {}'.format(name))
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = todolists_pb2_grpc.TodoListsStub(channel)
            response = stub.Create(todolists_pb2.CreateListRequest(name=name))
        print("Created TodoList with id {} and name {}".format(response.id, response.name))
        return response
    except _InactiveRpcError as e:
        print('Error creating TodoList')
        if e.args[0].code == StatusCode.UNAVAILABLE:
            print('Seems that the gRPC Server is Unavailable. - {}'.format(e.args[0].details))
        elif e.args[0].code == StatusCode.INVALID_ARGUMENT:
            print(e.args[0].details)
        else:
            print(e.args[0].details)


if __name__ == '__main__':
    create_list('TestList')
