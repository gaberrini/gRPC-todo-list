"""
This module is used to invoke the gRPC todolists.TodoLists.List Stub

Examples:
        This module can be executed as a script, this way it will execute the todolists.TodoLists.List Stub,
        it expects two positional arguments to define the `page_number` and `page_size`.
        If the arguments are not provided they will be requested by user input

            $ python stub_get_lists_paginated.py 1 10

        The module can also be imported to call the `get_lists_paginated` function and invoke the .List Stub.

            $ from proto_client.stub_get_lists_paginated import get_lists_paginated
            $ get_lists_paginated(page_number=1, page_size=10, grpc_channel)

Attributes:
    stub_get_lists_paginated.get_lists_paginated (function):
     Function use to invoke the gRPC to get the TodoLists paginated
"""
import os
import sys
from grpc._channel import _InactiveRpcError, Channel
from grpc import StatusCode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import proto.v1.todolists_pb2 as todolists_pb2  # pylint: disable=wrong-import-position
import proto.v1.todolists_pb2_grpc as todolists_pb2_grpc  # pylint: disable=wrong-import-position
from config.config import GRPC_SERVER_PORT  # pylint: disable=wrong-import-position
from proto_client.helpers import get_input, create_secured_client_channel  # pylint: disable=wrong-import-position


def get_lists_paginated(page_number: int, page_size: int, channel: Channel) -> todolists_pb2.ListTodoListsReply:
    """
    Invoke the TodoLists.List gRPC to get the TodoLists paginated

    The gRPC method have a `MAX_PAGE_SIZE`, if the `page_size` requested is bigger it will be set to the max value

    If a negative `page_number` is send to the gRPC it will be set to 1.

    :param page_number: desired page number
    :param page_size: desired page size
    :param channel: gRPC channel used to invoke the Stub

    :return: ListTodoListsReply

    :raise _InactiveRpcError:
        If the gRPC server is UNAVAILABLE
    """
    print('Calling TodoLists.List with `page_number={}` and `page_size={}`'.format(page_number, page_size))
    try:
        stub = todolists_pb2_grpc.TodoListsStub(channel)
        response = stub.List(todolists_pb2.ListTodoListsRequest(page_size=page_size, page_number=page_number))
        print('Response: `next_page_number={}` - `count={}`\n`todo_lists={}`'.format(response.next_page_number,
                                                                                     response.count,
                                                                                     response.todo_lists))
        return response
    except _InactiveRpcError as ex:
        exception_code = ex.args[0].code  # pylint: disable=no-member
        exception_details = ex.args[0].details  # pylint: disable=no-member
        if exception_code == StatusCode.UNAVAILABLE:
            print('Seems that the gRPC Server is Unavailable. - {}'.format(exception_details))
        else:
            print('Error getting TodoLists paginated - {}'.format(exception_details))
            raise ex


def main():
    """
    Main when executed as script
    :return:
    """
    # Expected two positional arguments, first `page_number`, second `page_size`
    try:
        _page_number = sys.argv[1]
        _page_size = sys.argv[2]
    except IndexError:
        _page_number = int(get_input('Please insert the desired page_number: ').strip())
        _page_size = int(get_input('Please insert the desired page_size: ').strip())
    with create_secured_client_channel('localhost:{}'.format(GRPC_SERVER_PORT)) as _channel:
        get_lists_paginated(page_number=int(_page_number), page_size=int(_page_size), channel=_channel)


if __name__ == '__main__':
    main()
