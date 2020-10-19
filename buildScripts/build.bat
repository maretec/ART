set /p path=Enter Python3 exe path: 
%path% -m pip install pipenv 
%path% -m pipenv install --ignore-pipfile --python %path%
%path% -m pipenv run pyinstaller --onefile ../python/art.py
pause