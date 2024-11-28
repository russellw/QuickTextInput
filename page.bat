cl /EP index.html >a.html||exit /b
call html-minifier a.html --collapse-whitespace --minify-css --remove-optional-tags --remove-attribute-quotes -o \t\index.html||exit /b
