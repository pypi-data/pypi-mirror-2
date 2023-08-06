#! /bin/sh

I18NDOMAIN="betahaus.memberprofile"

# See http://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
i18ndude rebuild-pot --pot locales/${I18NDOMAIN}.pot \
    --merge locales/manual.pot \
    --create ${I18NDOMAIN} \
   .

# sync the plone domain for workflows too
#i18ndude rebuild-pot --pot i18n/plone-${I18NDOMAIN}.pot \
#    --create plone \
#   ./profiles/default/workflows

# Synchronise the resulting .pot with all .po files
for po in locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    i18ndude sync --pot locales/${I18NDOMAIN}.pot $po
done

# same for the plone domain in i18n
#for po in i18n/plone-${I18NDOMAIN}-*.po; do
#    i18ndude sync --pot i18n/plone-${I18NDOMAIN}.pot $po
#done
