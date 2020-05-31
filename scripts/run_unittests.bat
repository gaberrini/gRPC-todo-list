cd %~dp0
cd ..

SET ENVIRONMENT=testing
pipenv run python -m unittest discover -s ./src --verbose
