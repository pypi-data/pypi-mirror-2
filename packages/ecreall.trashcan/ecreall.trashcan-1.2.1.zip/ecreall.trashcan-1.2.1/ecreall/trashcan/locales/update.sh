domain=ecreall.trashcan
i18ndude rebuild-pot --pot locales/$domain.pot --create $domain .
i18ndude sync --pot locales/$domain.pot locales/*/LC_MESSAGES/$domain.po

#i18ndude rebuild-pot --pot locales/plone.pot --create plone profiles
#i18ndude filter locales/plone.pot ../../../../eggs/plone.app.locales*/plone/app/locales/i18n/plone.pot > locales/plone.pot_
#mv locales/plone.pot_ locales/plone.pot
#i18ndude sync --pot locales/plone.pot i18n/$domain-plone-*.po
