python -m pip install --upgrade pip
pip install pyinstaller
pip install tabulate
pyinstaller lab3/lab3.py -y --onefile --distpath ../exe/lab3 --specpath ../specs
echo Процесс установки завершен
cmd /k