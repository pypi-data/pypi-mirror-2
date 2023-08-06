#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot Products.PyConBrasil.pot --create Products.PyConBrasil --merge manual.pot ..

# finally, update the po files
i18ndude sync --pot Products.PyConBrasil.pot  `find . -iregex '.*Products.PyConBrasil\.po$'|grep -v plone`

