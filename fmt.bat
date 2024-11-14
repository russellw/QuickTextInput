rem Python
black .||exit /b
isort .||exit /b
for %%x in (*.py) do blank-before-comment-py -w %%x||exit /b
for %%x in (*.py) do capitalize-comments-py -w %%x||exit /b
for %%x in (*.py) do sort-fns-py -w %%x||exit /b

rem HTML
call js-beautify --end-with-newline -t *.html -r||exit /b

git diff
