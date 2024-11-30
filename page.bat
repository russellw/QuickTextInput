cl /EP index.html >\t\a.html||exit /b
call html-minifier \t\a.html --collapse-whitespace --minify-css --remove-optional-tags --remove-attribute-quotes -o site\index.html||exit /b
