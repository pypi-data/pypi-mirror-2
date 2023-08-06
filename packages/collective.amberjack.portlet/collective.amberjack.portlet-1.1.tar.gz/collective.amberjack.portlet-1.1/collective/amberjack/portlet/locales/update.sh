i18ndude rebuild-pot --pot collective.amberjack.portlet.pot --create collective.amberjack.portlet --merge collective.amberjack.portlet-manual.pot ../
i18ndude sync --pot collective.amberjack.portlet.pot ./*/LC_MESSAGES/collective.amberjack.portlet.po

i18ndude rebuild-pot --pot ../i18n/collective.amberjack.portlet-plone.pot --create plone ../profiles
i18ndude sync --pot ../i18n/collective.amberjack.portlet-plone.pot ../i18n/collective.amberjack.portlet-plone-*.po
