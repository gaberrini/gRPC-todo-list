cd %~dp0
cd ..

set list-name=%1

if "%list-name%"=="" set list-name=TestList

echo Creating list with name "%list-name%"

pipenv run .\src\proto_client\create_list_stub.py %list-name%
