::vars
SET "root=C:\dev\dan-checker"
SET "virt=Z:\"
SET "name=Dan Checker"
:: set root
cd %root%
:: ensure newest commit
git pull
:: pyinstaller magic
pyinstaller "%root%\src\main.py" ^
--name "%name%" ^
--onefile ^
--windowed ^
--icon="%root%\build\icons\receipt_new.ico" ^
--distpath="bin\" ^
--log-level INFO
:: move to virtiofs share
copy "%root%\bin\%name%.exe" "%virt%"
