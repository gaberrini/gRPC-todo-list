# gRPC Todo Lists
First project to try gRPC using Python.

This project has been developed to test gRPC. It has not been developed with the best practices.

This started the [gRPC Quick Start Tutorial] for Python. If you are new with this technologies you can read about [gRPC].

# Prerequisites

[Python 3.7] Interpreter

[Pipenv] Packages manager

# Install dependencies

After installing the prerequisites, you must install the dependencies with the following command

```
pipenv install
```

# Running the Server-Client

## Server

To run the server you need to execute the following command

```
pipenv run .\src\run_grpc_server.py
```

## Client

To run the test client you need to execute the following command, for the client to work successfully the gRPC server must be running.

The test client will try the different gRPC available.

```
pipenv run .\src\proto_client\todolists_client.py
```

# Changing Proto Services and Stubs

If you don't know how gRPC and protocol buffers works you can start reading about [gRPC] for more information.

The proto Services and Stubs are defined in .proto files located at

```
./api/proto
```

After changing a service or a stub you need to compile the protocol buffer files to generate the new python code for them.

To run the [protocol buffers compiler] you must run the following command

```
pipenv run python -m grpc_tools.protoc -I./api --python_out=./src --grpc_python_out=./src [PROTOS_FILE_PATH]
```

You must specify the proto files that you want to compile changing `[PROTOS_FILES_PATH]`. The output files will be generated after running the command. The destination folder is specify in the command.

For example to compile the `todolists.proto` file you must run

```
pipenv run python -m grpc_tools.protoc -I./api --python_out=./src --grpc_python_out=./src ./api/proto/v1/todolists.proto
```

[Python 3.7]: https://www.python.org/downloads/
[Pipenv]: https://pipenv-fork.readthedocs.io/en/latest/
[gRPC Quick Start Tutorial]: https://grpc.io/docs/languages/python/quickstart/
[gRPC]: https://grpc.io/docs/guides/
[protocol buffers compiler]: https://developers.google.com/protocol-buffers/docs/proto#generating
