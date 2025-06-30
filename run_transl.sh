#!/bin/bash

FASTA_DIR="/Users/haleyatkins/Desktop/109_pop/proteins"

SCRIPT_PATH="/Users/haleyatkins/Desktop/109_pop/translate_fasta.py"
for file in "$FASTA_DIR"/*.fasta; do
    echo "Processing $file..."
    python3 "$SCRIPT_PATH" "$file"
done
