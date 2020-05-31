cd %~dp0
cd ..

set page-number=%1
set page-size=%2

echo Fetching lists with page-number "%page-number%" and page-size "%page-size%"

pipenv run .\src\proto_client\stub_get_lists_paginated.py %page-number% %page-size%
