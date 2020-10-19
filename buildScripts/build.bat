python -m pip install pipenv
python -m pipenv install --ignore-pipfile
python -m pipenv run pyinstaller --onefile ../python/art.py
pause