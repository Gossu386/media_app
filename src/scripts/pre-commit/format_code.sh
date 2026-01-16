#!/bin/bash
set -e # Exit on error

OUT="ruff_txt_output.txt"
echo "Ruff run at $(date)" > $OUT
echo "" >> $OUT
echo "PWD:" >> $OUT && pwd >> $OUT
echo "" >> $OUT
echo "ls:" >> $OUT && ls >> $OUT

# Format the code using ruff
echo "== Ruff check --fix and format ==" >> $OUT
echo "" >> $OUT
'.venv/bin/ruff' check src --fix | tee -a "$OUT"
echo "" >> $OUT
'.venv/bin/ruff' format src | tee -a "$OUT"

echo "✓ Ruff formatting completed successfully" >> $OUT
