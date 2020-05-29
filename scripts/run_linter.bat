cd %~dp0
cd ..

pipenv run python -m pylint src
