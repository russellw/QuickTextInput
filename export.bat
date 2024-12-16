cl /EP index.html >\t\z.html||exit /b
call js-beautify --end-with-newline -t \t\z.html -r||exit /b
