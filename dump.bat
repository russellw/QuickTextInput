if not exist C:\Users\User\Documents\QuickTextInput.db exit /b
sqlite3 C:\Users\User\Documents\QuickTextInput.db .dump|head -n 30
