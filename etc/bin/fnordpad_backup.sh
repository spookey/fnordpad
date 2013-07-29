#!/bin/bash

rsync --partial --progress --stats -h --rsh=ssh -r fnord:/srv/www/fnordpad/content $HOME
