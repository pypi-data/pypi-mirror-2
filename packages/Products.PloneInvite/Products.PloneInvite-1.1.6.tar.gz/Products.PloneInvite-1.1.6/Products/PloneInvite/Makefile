I18N_DOMAIN = PloneInvite

default:help
	@echo "Nothing to do by default."
	@echo "Use 'make pot' to create or update .pot from skins directory."
	@echo "Use 'make xx.po' to create or update translation file from .pot, where xx is your language."

help:
	@echo
	@echo "-----------------------------------------------------------"
	@echo " Makefile Manual for ${I18N_DOMAIN} L10n                   "
	@echo "-----------------------------------------------------------"
	@echo "                                                           "
	@echo " This Makefile have the bellows taks:                      "
	@echo "-----------------------------------------------------------"
	@echo " help     - show the Makefle taks for ${I18N_DOMAIN} L10n  "
	@echo " clean    - remove the files generated                     "
	@echo " pot      - Rebuild the master template from source code   "
	@echo " %.po     - Update a specify po file, for example: es.po   "
	@echo " all-po   - Update all po file for every l10n              "
	@echo " validate - Validate all the template to find-untranslated "
	@echo " all      - Run almost all generic Makefle taks            "
	@echo "-----------------------------------------------------------"
	@echo

clean:
	rm -f .*~ *~ *.tgz *.bak *.hi *.ho `find . -name "*.pyc"`
	rm -f ./i18n/*.mo ./i18n/*.diff ./i18n/*.backup ./skins/dtmlmessages.pt ./i18n/rebuild_i18n.log

# Create or update a {i18ndomain}.pot file
pot:

	touch ./skins/dtmlmessages.pt
	# DTML extraction hack
	echo '<div i18n:domain="${I18N_DOMAIN}">' > ./skins/dtmlmessages.pt 
	find ./dtml -name "*dtml" | xargs perl -n -e '/<dtml-translate domain="?${I18N_DOMAIN}"? msgid="?(.*?)"?>(.*?)<\/dtml-translate>/ and print "<span i18n:translate=\"$$1\">$$2<\/span>\n";' >> ./skins/dtmlmessages.pt
	echo '</div>' >> ./skins/dtmlmessages.pt

	touch ./i18n/${I18N_DOMAIN}.pot

	# Back up the existing file
	cp ./i18n/${I18N_DOMAIN}.pot ./i18n/${I18N_DOMAIN}.pot.backup
#	i18ndude rebuild-pot --pot ./i18n/${I18N_DOMAIN}.pot \
#		--create ${I18N_DOMAIN} ./skins/ploneinvite/
#	i18ndude merge --pot ./i18n/${I18N_DOMAIN}.pot --merge ./i18n/base.pot
#	i18ndude rebuild-pot --pot ./i18n/plone.pot --create plone  ./skins/
	i18ndude rebuild-pot --pot ./${I18N_DOMAIN}.pot \
                --create ${I18N_DOMAIN} \
                --merge ./i18n/base.pot \
                --exclude=`find ./skins/ploneinvite/ -name "*.*py"` ./ ./skins/
	i18ndude rebuild-pot --pot ./i18n/plone.pot --create plone ./skins/ploneinvite/

# Update translation files {i18ndomain}-{xx}.pot
# and plone-{xx}.pot, creating them if needed.
%.po: pot
	touch ./i18n/${I18N_DOMAIN}-$*.po

	# Back up the existing file
	cp ./i18n/${I18N_DOMAIN}-$*.po ./i18n/${I18N_DOMAIN}-$*.po.backup
	i18ndude sync --pot ./i18n/${I18N_DOMAIN}.pot ./i18n/${I18N_DOMAIN}-$*.po

	# And for the plone domain translations, too.
	touch ./i18n/plone-$*.po
	cp ./i18n/plone-$*.po ./i18n/plone-$*.po.backup

	# Note that we assume that there's a 'plone.pot' file in 'i18n/'.
	i18ndude sync --pot ./i18n/plone.pot ./i18n/plone-$*.po

all-po:
	# Syncronize message file for PloneInvite > ./i18n/PloneInvite-*.pot
	i18ndude sync --pot ./i18n/${I18N_DOMAIN}.pot ./i18n/${I18N_DOMAIN}-*.po

	# Syncronize message file for PloneInvite > ./i18n/PloneInvite-plone-*.po
	i18ndude sync --pot ./i18n/plone.pot ./i18n/plone-*.po

validate:
	WARNINGS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-WARN' | wc -l`
	ERRORS=`find . -name "*pt" | xargs i18ndude find-untranslated | grep -e '^-ERROR' | wc -l`
	FATAL=`find . -name "*pt"  | xargs i18ndude find-untranslated | grep -e '^-FATAL' | wc -l`

	echo "\n"
	echo "There are ${WARNINGS} warnings \(possibly missing i18n markup\)"
	echo "There are ${ERRORS} errors \(almost definitely missing i18n markup\)"
	echo "There are ${FATAL} fatal errors \(template could not be parsed, eg. if it\'s not html\)"
	echo "For more details, run \'find . -name \"\*pt\" \| xargs i18ndude find-untranslated\' or" 
	echo "Look the rebuild i18n log generate for this script called \'rebuild_i18n.log\' on i18n dir" 

	touch ./i18n/rebuild_i18n.log

	find ./ -name "*pt" | xargs i18ndude find-untranslated > ./i18n/rebuild_i18n.log

all: clean pot all-po validate

