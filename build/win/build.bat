SET "root=C:/dev/dan-checker"
SET "virt=Z:/"
SET "name=Dan Checker"

cd %root%
:: ensure newest commit
git pull
:: pyinstaller magic
pyinstaller "%root%/src/main.py" ^
--name "%name%" ^
--onefile ^
--windowed ^
--icon="./build/icons/receipt-new.ico" ^
--distpath="bin/" ^
--log-level INFO
:: move to virtiofs share
COPY "%root%/bin/%name%.exe" %virt%
