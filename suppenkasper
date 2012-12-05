#!/bin/bash

# Kein Kommentar #

## Variablen
# Zielordner der Bilder
ordner=$HOME/bilder
# Namen der soups
suppe=(fnordpad gnd cccmz sixtus fotochaoten kochchaoten hipsterhackers)

soupfeed() {
	# Adresse zusammenstückeln
	url=http://${name}.soup.io/rss/
	wget -qO - $url | grep -o '<enclosure [^>]*>' | grep -o 'http://[^\"]*'  | sed 's/_[0-9][0-9][0-9]\././' | sed 's/\.jpeg/.jpg/'
}

soupweb() {
	# Wie viele Seiten soll ich gehen?
	if [ -z $2 ]; then
		pages=5
	else
		pages=$2
	fi

	for ((i=0; i<pages; i++)); do
		# Adresse zusammenstückeln
		url=http://${name}.soup.io/${since}
		wget -qO - $url | grep -o 'http://[0-9a-z].asset.soup.io/asset/[^0000][^\"]*' | grep -wv square* | sed 's/_[0-9][0-9][0-9]\././' | sed 's/_[0-9][0-9]\././' | sed 's/\.jpeg/.jpg/'
		# Umblättern
		since=$(wget -qO - $url | grep -w 'SOUP.Endless.next_url' | grep -o 'since[^?;]*' )
	done
}

# Bilderordner anlegen, falls er nicht existiert
if [ ! -d "$ordner" ]; then
  mkdir -p $ordner
fi

for name in ${suppe[@]}; do

	# die rss Feeds parsen
	wget -qc -P $ordner $(soupfeed $name)

	# die Reposts von der Seite holen
	wget -qc -P $ordner $(soupweb $name)

done

exit 0
