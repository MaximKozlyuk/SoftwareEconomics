python -m pip install --upgrade pip
pip install pyinstaller
pip install matplotlib
pip install tabulate
pyinstaller lab4/lab4.py -y --onefile --distpath ../exe/lab4 --specpath ../specs
echo Процесс установки завершен
cmd /k