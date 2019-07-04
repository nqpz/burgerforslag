#!/bin/sh

set -e
cd "$(dirname "$0")"

./get_all_ids.py | while read id; do
    if ! test -f text/$id.json; then
        ./generate_text.sh id $id
    fi
done
