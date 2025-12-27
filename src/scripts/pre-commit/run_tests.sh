#!/bin/bash
set -e # Exit on error

OUT="pytest_txt_output.txt"
echo "Run pytest at $(date)" > $OUT
echo "PWD:" >> $OUT && pwd >> $OUT
echo "" >> $OUT
echo "ls:" >> $OUT && ls >> $OUT
echo "" >> $OUT

# Run tests using pytest
echo "== Running Pytest ==" >> $OUT
echo "" >> $OUT
'.venv/bin/pytest' src/tests | tee -a "$OUT"
echo "" >> $OUT
echo "✓ Pytest completed successfully" >> $OUT