call page.bat
timestamp-html -w site\index.html
upload-s3 quicktextinput.com site\index.html
invalidate quicktextinput.com
