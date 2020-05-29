cd %~dp0
cd ..\src

pipenv run python -m unittest --verbose
