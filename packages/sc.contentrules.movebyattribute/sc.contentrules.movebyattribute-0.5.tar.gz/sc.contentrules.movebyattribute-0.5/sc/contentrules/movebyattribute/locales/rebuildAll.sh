#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot sc.contentrules.movebyattribute.pot --create sc.contentrules.movebyattribute --merge manual.pot ..

# finally, update the po files
i18ndude sync --pot sc.contentrules.movebyattribute.pot  `find . -iregex '.*sc.contentrules.movebyattribute\.po$'|grep -v plone`

