black .||exit /b
isort .||exit /b
for %%x in (*.py) do blank-before-comment-py -w %%x||exit /b
git diff
