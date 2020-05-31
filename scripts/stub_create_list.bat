cd %~dp0
cd ..

set list-name=%1

echo Creating list with name "%list-name%"

pipenv run .\src\proto_client\stub_create_list.py %list-name%
