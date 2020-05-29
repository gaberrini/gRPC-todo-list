"""
This module is used to invoke the gRPC todolists.TodoLists.Create Stub

Examples:
        This module can be executed as a script, this way it will execute the todolists.TodoLists.Create Stub,
        it accept an optional positional argument to define the new List name. If no argument is defined
        it will try to create a List with the name `TestList`

            $ python create_list_stub.py NewListName

        The module can also be imported to call the `create_list` function and invoke the .Create Stub.

            $ from proto_client.create_list_stub import create_list
            $ create_list('new_list_name', grpc_channel)

Attributes:
    create_list (function): Function use to invoke the gRPC to create a new TodoList
"""
import grpc
import os
import sys
from typing import Optional
from grpc._channel import _InactiveRpcError, Channel
from grpc import StatusCode

# Not good practice, add src to python path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import proto.v1.todolists_pb2 as todolists_pb2
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc


def create_list(name: str, channel: Channel) -> Optional[todolists_pb2.CreateListReply]:
    """
    Invoke the TodoLists.Create gRPC to create a new List with the defined name

    :param name: name for the new list
    :param channel: gRPC channel used to invoke the Stub

    :return: CreateListReply of invoked stub

    :raise :

    """
    print('Calling TodoLists.Create with name {}'.format(name))
    try:
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
        raise e


if __name__ == '__main__':
    # New list name can be specified by positional arguments, if not default is used
    try:
        new_list_name = sys.argv[1]
    except IndexError:
        new_list_name = 'TestList'
    with grpc.insecure_channel('localhost:50051') as _channel:
        create_list(new_list_name, _channel)
