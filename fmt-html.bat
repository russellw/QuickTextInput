call js-beautify --end-with-newline -t index.html -r||exit /b
sort-html-attrs -w index.html||exit /b
git diff
