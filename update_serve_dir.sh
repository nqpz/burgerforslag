#!/bin/sh

set -e
cd "$(dirname "$0")"

mkdir -p serve/se-og-stoet-forslag/

# You need a webserver configuration like this:
#
#   location /se-og-stoet-forslag {
#      try_files $uri "${uri}_${args}.html" =404;
#   }
ls html | while read fname; do
    ln -fs "../../html/$fname" "serve/se-og-stoet-forslag/_Id=FT-$fname"
done

ln -fs ../style.css ../script.js ../logo.png serve/
