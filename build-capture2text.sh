QT_SELECT=5 qmake Capture2Text/Capture2Text.pro -d
make
wget "https://github.com/GSam/Capture2Text/releases/download/Prototype/English.zip"
unzip -o "English.zip" -d "tessdata"
rm "English.zip"
