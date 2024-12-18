pp index.html >\t\z.html||exit /b
minify-class-names -w \t\z.html||exit /b
call html-minifier \t\z.html --collapse-whitespace --minify-css --remove-optional-tags --remove-attribute-quotes --minify-js -o site\index.html||exit /b
