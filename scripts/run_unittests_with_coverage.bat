cd %~dp0
cd ..\src

pipenv run python -m coverage run -m unittest --verbose
pipenv run python -m coverage report
pipenv run python -m coverage html
