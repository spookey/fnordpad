#!/bin/bash

# Kein Kommentar #

## Variablen
# Zielordner der Bilder
ordner=$HOME/Desktop/bilder
# Soup Parser
sparser=./soup-parser.py  
# Namen der soups
suppe=(fnordpad gnd cccmz sixtus fotochaoten kochchaoten hipsterhackers)

# Bilderordner anlegen, falls er nicht existiert
if [ ! -d "$ordner" ]; then
  mkdir -p $ordner
fi

for name in ${suppe[@]}; do

	# die rss Feeds parsen
	wget -c -P $ordner $($sparser $name)
	
done

exit 0