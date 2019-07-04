#!/bin/sh

set -e
cd "$(dirname "$0")"

type="$1"
if [ "$type" = id ]; then
    id="$2"
    url="https://www.borgerforslag.dk/se-og-stoet-forslag/?Id=FT-$id"
elif [ "$type" = url ]; then
    url="$2"
    id="$(echo $url | grep -Eo 'Id=[^&]+' | cut -d- -f2)"
fi

mkdir -p text

./rødløg.py "$url" > text/$id.json
