md \t\32x32
cd \t\32x32
copy \icons\svgs||exit /b
for %%x in (*.svg) do \svg-to-png\bin\Release\net8.0\win-x64\svg-to-png.exe %%x 32 32||exit /b
del *.svg
