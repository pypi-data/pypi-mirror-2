#!/bin/sh

#This script must be executed from the product folder.
#i18ndude should be available in current $PATH

i18ndude rebuild-pot --pot locales/getpaid.nullpayment.pot --create getpaid.nullpayment --merge locales/manual.pot ./

for file in `find locales -name *.po`
do
    echo Syncing $file ...
    i18ndude sync --pot locales/getpaid.nullpayment.pot $file
    msgfmt -o `dirname $file`/`basename $file .po`.mo $file
done
