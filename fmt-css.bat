css-comment -w styles.css||exit /b
call js-beautify --end-with-newline -t styles.css -r||exit /b
git diff
