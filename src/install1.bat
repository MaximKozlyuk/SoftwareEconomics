python -m pip install --upgrade pip
pip install pyinstaller
pyinstaller lab1.py -y --onefile --distpath ../exe --specpath ../specs
echo Процесс установки завершен
cmd /k