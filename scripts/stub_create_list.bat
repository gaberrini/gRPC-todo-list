cd %~dp0
cd ..

set list-name=%1

if "%list-name%"=="" set list-name=TestList

echo Creating list with name "%list-name%"

pipenv run .\src\proto_client\stub_create_list.py %list-name%
