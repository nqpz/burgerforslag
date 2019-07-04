#!/bin/sh

set -e
cd "$(dirname "$0")"

./generate_missing_ids.sh

ls text/ | while read fname; do
    id=$(basename $fname .json)
    if ! test -f html/$id.html; then
        ./generate_html_proposal.py $id
    fi
done

./generate_html_overview.py > serve/index.html
./update_serve_dir.sh
