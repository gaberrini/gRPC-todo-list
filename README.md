# gRPC Todo Lists
This project has been developed to practice the use of gRPC.

This started the [gRPC Quick Start Tutorial] for Python. If you are new with this technologies you can read about [gRPC].

# Index

* [Prerequisites](#prerequisites)
* [Install dependencies](#install-dependencies)
* [Running the Server-Client Stubs](#running-the-server-client-stubs)
    * [Environment variables](#environment-variables)
    * [Server](#server)
    * [Client Stubs](#client-stubs)
* [Running tests, tests coverage and linter](#running-tests-tests-coverage-and-linter)
    * [Run unittests](#run-unittests)
    * [Run unittests with coverage](#run-unittests-with-coverage)
    * [Run linter pylint](#run-linter-pylint)
* [Running Scripts](#running-scripts)
    * [Run gRPC server](#run-grpc-server)
    * [Run Create List stub](#run-create-list-stub)
    * [Run Get List stub](#run-get-list-stub)
    * [Run unittests script](#run-unittests-script)
    * [Run unittests with coverage script](#run-unittests-with-coverage-script)
    * [Run linter pylint script](#run-linter-pylint-script)
* [Changing Proto Services and Stubs](#changing-proto-services-and-stubs)

# Prerequisites

[Python 3.7] Interpreter

[Pipenv] Packages manager

# Install dependencies

After installing the prerequisites, you must install the dependencies with the following command

```
pipenv install
```

## Development dependencies

To install development dependencies to [run tests](#run-unittests), see [test coverage](#run-unittests-with-coverage), and run the [linter pylint](#run-linter-pylint), you must run the following command

```
pipenv install --dev
```

# Running the Server-Client Stubs

## Environment variables

* **GRPC_SERVER_PORT**: Used by the gRPC server to listen to this port, and stubs to connect to the server.

## Server

You can start the server running the `.bat` file [run_grpc_server.bat](#run-grpc-server)

To run the server you need to execute the following command

```
pipenv run .\src\run_grpc_server.py
```

## Client Stubs

### New list stub

You can execute the new list stub running the `.bat` file [stub_create_list.bat](#run-create-list-stub)

This script will create a new list calling the `TodoLists.Create` stub. For the stub to work successfully the gRPC server must be running.

The script accept an optional parameter to define the desired list `name`, if no parameter is defined it will try to create a list with `name=TestList`

To run the create list stub you need to execute the following command:

```
pipenv run .\src\proto_client\stub_create_list.py listname
```

The list names must be unique. If the list `name` already exist, the stub will fail and show an error message.

### Fetch list stub

You can execute the fetch list stub running the `.bat` file [stub_get_list.bat](#run-get-list-stub)

This script will get a list by `id` calling the `TodoLists.Get` stub.

The script accept an optional parameter to define the desired list `id`, if no parameter is defined it will try to get a list with `id=1`

To run the get list stub you need to execute the following command:

```
pipenv run .\src\proto_client\stub_get_list.py id
```

If a list with that `id` does not exist, the stub will fail and show an error message.

# Running tests, tests coverage and linter

## Run unittests

The project comes with `unittests` you can execute them with the script [run_unittests.bat](#run-unittests-script)

If you prefer you can run them manually.

```
pipenv run python -m unittest discover -s ./src --verbose
```

## Run unittests with coverage

You can run the `unittests` and see the `tests coverage`. You can do it running the script [run_unittests_with_coverage.bat](#run-unittests-with-coverage-script)

If you prefer you can run them manually.

```
pipenv run python -m coverage run -m unittest discover -s ./src --verbose
```

The last command will create the `coverage` results. To display them in terminal you must run

```
pipenv run python -m coverage report
```

You can also create a `HTML report` running the following command

```
pipenv run python -m coverage html
```

After running it a `HTML report` will be created, you can find it in the following path `./htmlcov/index.html`

## Run linter pylint

When doing changes to the codebase you can validate the coding standards with `pylint`. To do it you can run the script [Run linter pylint script](#run-linter-pylint-script)

To do it manually you can run the following command

```
pipenv run pylint src
```

# Running Scripts

In the folder `/scripts` you can find different `.bat` scripts with different goals

## Run gRPC server

This script will run the gRPC server

```
./scripts/run_grpc_server.bat
```

## Run Create List stub

This script will execute the stub to create a new List `TodoLists.Create`

The script accept an optional parameter to define the List `name` to be created, if no parameter is defined it will create a list with the `name=TestList`

```
./scripts/stub_create_list.bat ListName
```

## Run Get List stub

This script will get a List by `id` with the stub `TodoLists.Get`

The script accept an optional parameter to define the List `id` to get, if no parameter is defined it will get a list with `id=1`

```
./scripts/stub_get_list.bat id
```

## Run unittests script

This script will run the `unittests`

```
./scripts/run_unittests.bat
```

## Run unittests with coverage script

This script will run the `unittests` and show the tests `coverage`

The `coverage report` will be display in the `terminal`.

```
./scripts/run_unittests_with_coverage.bat
```

A `HTML report` will be created, you can find it in the following path `./htmlcov/index.html`

## Run linter pylint script

This script will run `pylint` to check the coding standards of the base code, the results will be display in the terminal.

```
./scripts/run_linter.bat
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
