if not exist C:\Users\User\Documents\TypeSmart.db exit /b
sqlite3 C:\Users\User\Documents\TypeSmart.db .dump|head -n 30
