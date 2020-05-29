cd %~dp0
cd ..

pipenv run python -m unittest discover -s ./src --verbose
