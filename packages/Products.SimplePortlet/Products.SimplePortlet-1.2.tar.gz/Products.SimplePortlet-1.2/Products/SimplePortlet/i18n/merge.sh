#!/bin/bash

echo "Syncing SimplePortlet domain PO files..."
for PO in simpleportlet-*.po; do
  echo $PO
  i18ndude sync --pot simpleportlet.pot $PO
done
echo "done."
echo ""

echo "Syncing plone domain PO files..."
for PO in plone-simpleportlet-*.po; do
  echo $PO
  i18ndude sync --pot plone-simpleportlet.pot $PO
done
echo "done."
