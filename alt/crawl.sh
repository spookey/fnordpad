#ugly code is ugly#
#!/bin/bash

## create temporary files
echo "" > ~/loadlist
echo "#!/bin/bash" > ~/load.sh

## parsing feeds
curl -s http://sixtus.soup.io/rss | grep -w "enclosure type=\"image/jpeg\"" | awk 'BEGIN {FS = "url=\""} {print $2}' | awk 'BEGIN {FS = "\""} {print $1}' | awk '{ sub(/_400/, ""); print }' | awk '{ sub(/.jpeg/, ".jpg"); print }' >> ~/loadlist

curl -s http://fnordpad.soup.io/rss | grep -w "enclosure type=\"image/jpeg\"" | awk 'BEGIN {FS = "url=\""} {print $2}' | awk 'BEGIN {FS = "\""} {print $1}' | awk '{ sub(/_400/, ""); print }' | awk '{ sub(/.jpeg/, ".jpg"); print }' >> ~/loadlist

curl -s http://fotochaoten.soup.io/rss | grep -w "enclosure type=\"image/jpeg\"" | awk 'BEGIN {FS = "url=\""} {print $2}' | awk 'BEGIN {FS = "\""} {print $1}' | awk '{ sub(/_400/, ""); print }' | awk '{ sub(/.jpeg/, ".jpg"); print }' >> ~/loadlist

curl -s http://gnd.soup.io/rss | grep -w "enclosure type=\"image/jpeg\"" | awk 'BEGIN {FS = "url=\""} {print $2}' | awk 'BEGIN {FS = "\""} {print $1}' | awk '{ sub(/_400/, ""); print }' | awk '{ sub(/.jpeg/, ".jpg"); print }' >> ~/loadlist

## generating download list
echo "cd ~/bilder/" >> ~/load.sh
cat ~/loadlist | awk '{ sub(/http:/, "curl -sfO http:"); print }' >> ~/load.sh

echo "rm ~/bilder/*gif" >> ~/load.sh

## start downloads
chmod +x ~/load.sh
exec ~/load.sh

## cleaning up
rm ~/loadlist ~/load.sh
