cl /EP index.html >\t\z.html||exit /b
call html-minifier \t\z.html --collapse-whitespace --minify-css --remove-optional-tags --remove-attribute-quotes -o site\index.html||exit /b
