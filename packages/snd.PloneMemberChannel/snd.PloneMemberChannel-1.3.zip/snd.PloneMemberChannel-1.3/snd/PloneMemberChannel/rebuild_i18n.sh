#!/bin/bash

I18NDUDE="i18ndude"
PRODUCTNAME="snd.PloneMemberChannel"
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the python code.
$I18NDUDE rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the Dutch .po files
for po in $(find locales -name ${PRODUCTNAME}.po); do
    echo $po
    $I18NDUDE sync --pot locales/${PRODUCTNAME}.pot $po
done
