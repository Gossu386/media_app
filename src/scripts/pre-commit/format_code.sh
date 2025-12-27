#!/bin/bash
OUT="ruff_txt_output.txt"
echo "Ruff run at $(date)" > $OUT
echo "" >> $OUT
echo "PWD:" >> $OUT && pwd
echo "" >> $OUT
echo "ls:" >> $OUT && ls >> $OUT

# Format the code using ruff
echo "== Ruff check --fix and format ==" >> $OUT
echo "" >> $OUT
"/home/dev/projects/media_app/.venv/bin/ruff" check src --fix | tee -a "$OUT"
echo "" >> $OUT
"/home/dev/projects/media_app/.venv/bin/ruff" format src | tee -a "$OUT"

