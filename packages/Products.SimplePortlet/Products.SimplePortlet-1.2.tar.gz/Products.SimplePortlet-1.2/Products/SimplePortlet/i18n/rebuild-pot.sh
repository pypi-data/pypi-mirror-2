#!/bin/bash

POT=simpleportlet.pot
MANUAL=manual.pot
DOMAIN=SimplePortlet

i18ndude rebuild-pot --pot $POT --create $DOMAIN --merge $MANUAL ../skins
echo "Rebuilt POT file into $POT"
echo ""
echo "Now you can run ./merge.sh to merge the POT changes with the po files."
echo ""
