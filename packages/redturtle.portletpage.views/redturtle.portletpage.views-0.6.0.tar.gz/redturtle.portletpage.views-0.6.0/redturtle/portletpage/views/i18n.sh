#!/bin/sh

PRODUCT='redturtle.portletpage.views'
DOMAIN='plone'

i18ndude merge --pot i18n/${PRODUCT}-${DOMAIN}.pot --merge i18n/${PRODUCT}-${DOMAIN}-manual.pot .
i18ndude sync --pot i18n/${PRODUCT}-${DOMAIN}.pot i18n/${PRODUCT}-${DOMAIN}-it.po
