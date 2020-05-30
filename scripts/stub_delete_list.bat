cd %~dp0
cd ..

set list-id=%1

if "%list-id%"=="" set list-id=1

echo Deleting list with id "%list-id%"

pipenv run .\src\proto_client\stub_delete_list.py %list-id%
