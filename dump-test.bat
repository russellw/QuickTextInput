if not exist test.db exit /b
sqlite3 test.db .dump|head -n 30
