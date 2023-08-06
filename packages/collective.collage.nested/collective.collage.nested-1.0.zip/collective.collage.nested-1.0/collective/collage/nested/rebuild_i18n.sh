#! /bin/sh

I18NDOMAIN="collective.collage.nested"
I18NDUDE="../../../../../bin/i18ndude"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
$I18NDUDE rebuild-pot --pot locales/${I18NDOMAIN}.pot \
    --create ${I18NDOMAIN} \
   .

# Synchronise the resulting .pot with all .po files
for po in locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    $I18NDUDE sync --pot locales/${I18NDOMAIN}.pot $po
done
