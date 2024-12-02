rem Python
black .||exit /b
isort .||exit /b
for %%x in (*.py) do blank-before-comment-py -w %%x||exit /b
for %%x in (*.py) do capitalize-comments-py -w %%x||exit /b
for %%x in (*.py) do sort-fns-py -w %%x||exit /b

rem HTML
call js-beautify --end-with-newline -t index.html -r||exit /b
sort-html-attrs -w index.html||exit /b

rem CSS
css-comment -w styles.css
call js-beautify --end-with-newline -t styles.css -r||exit /b

git diff
