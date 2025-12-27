#!/bin/bash

CORPUS_DIR="corpus_final"
OUTPUT_FILE="index.json"

echo "{" > $OUTPUT_FILE
echo "  \"generated_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> $OUTPUT_FILE
echo "  \"files\": [" >> $OUTPUT_FILE

FIRST=true

find "$CORPUS_DIR" -type f -name "*.txt" | sort | while read -r FILE; do
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "    ," >> $OUTPUT_FILE
    fi

    SHA=$(sha256sum "$FILE" | awk '{print $1}')
    SIZE=$(stat -c%s "$FILE")
    MODIFIED=$(date -r "$FILE" -u +"%Y-%m-%dT%H:%M:%SZ")

    echo "    {" >> $OUTPUT_FILE
    echo "      \"path\": \"$FILE\"," >> $OUTPUT_FILE
    echo "      \"sha256\": \"$SHA\"," >> $OUTPUT_FILE
    echo "      \"size_bytes\": $SIZE," >> $OUTPUT_FILE
    echo "      \"last_modified\": \"$MODIFIED\"" >> $OUTPUT_FILE
    echo "    }" >> $OUTPUT_FILE
done

echo "  ]" >> $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

echo "Index generated in $OUTPUT_FILE"


