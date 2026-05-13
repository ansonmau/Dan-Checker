pyinstaller "./src/main.py" ^
--name "Dan Checker" ^
--onefile ^
--windowed ^
--icon="./build/icons/receipt-new.ico" ^
--distpath="bin/" ^
--log-level INFO
