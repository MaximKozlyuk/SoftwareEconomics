python -m pip install --upgrade pip
pip install pyinstaller
pip install matplotlib
pip install sympy
pyinstaller lab2.py -y --onefile --distpath ../exe --specpath ../specs
echo Процесс установки завершен
cmd /k