cd %~dp0
cd ..

SET ENVIRONMENT=testing
pipenv run python -m coverage run -m unittest discover -s ./src --verbose
pipenv run python -m coverage report
pipenv run python -m coverage html
