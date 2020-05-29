cd %~dp0
cd ..

set list-id=%1

if "%list-id%"=="" set list-id=1

echo Fetching list with id "%list-id%"

pipenv run .\src\proto_client\stub_get_list.py %list-id%
