#!/bin/bash
OUT="pytest_txt_output.txt"
echo "Run pytest at $(date)" > $OUT
echo "PWD:" >> $OUT && pwd >> $OUT
echo "" >> $OUT
echo "ls:" >> $OUT && ls >> $OUT
echo "" >> $OUT

# Run tests using pytest
echo "== Pytest results ==" >> $OUT
echo "" >> $OUT
"/home/dev/projects/media_app/.venv/bin/pytest" src/tests | tee -a "$OUT"