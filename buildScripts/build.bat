set /p path=Enter Python3 folder exe path: 
%path%\python.exe -m pip install pipenv 
%path%\python.exe -m pipenv install --ignore-pipfile --python %path%
%path%\python.exe -m pipenv run pyinstaller --onefile ../python/art.py
pause