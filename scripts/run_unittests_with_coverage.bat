cd %~dp0
cd ..

pipenv run python -m coverage run -m unittest discover -s ./src --verbose
pipenv run python -m coverage report
pipenv run python -m coverage html
