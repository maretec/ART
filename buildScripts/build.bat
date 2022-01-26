::===============================================================
:: To define the Python3 folder path remove comment (::) from 
:: the following line and put the path to the folder.
::===============================================================

::set py_path=PATH/TO/PYTHONFOLDER 




::============================
:: DO NOT CHANGE BELOW THIS
::============================
if NOT DEFINED py_path set /p py_path=Python path not defined. Please enter Python3 folder exe path: 
%py_path%\python.exe -m pip install pipenv 
%py_path%\python.exe -m pipenv install --ignore-pipfile --python %py_path%\python.exe
%py_path%\python.exe -m pipenv run pyinstaller --onefile ../python/art.py --paths=../python/common/ --paths=../python/
pause
