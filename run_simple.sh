#!/bin/bash

echo "Cleaning temp files..."
find . -name .DS_Store | xargs rm

echo "Simple..."
FEATURES=""
for i in `find corpus -depth 1`; do
    FEATURES="$FEATURES -d $i"
done
python simple.py $FEATURES -t test
