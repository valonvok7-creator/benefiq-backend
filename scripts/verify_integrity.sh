#!/bin/bash

INDEX_FILE="index.json"

jq -c '.files[]' $INDEX_FILE | while read -r ITEM; do
    FILE=$(echo $ITEM | jq -r '.path')
    EXPECTED=$(echo $ITEM | jq -r '.sha256')

    if [ ! -f "$FILE" ]; then
        echo "❌ Missing file: $FILE"
        continue
    fi

    ACTUAL=$(sha256sum "$FILE" | awk '{print $1}')

    if [ "$EXPECTED" = "$ACTUAL" ]; then
        echo "✅ OK: $FILE"
    else
        echo "⚠️  MISMATCH: $FILE"
        echo "    expected: $EXPECTED"
        echo "    actual:   $ACTUAL"
    fi
done

