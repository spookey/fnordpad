#!/bin/bash

rsync --partial --progress --stats -h --rsh=ssh -r fnord:/var/www/fnordpad/content $HOME
