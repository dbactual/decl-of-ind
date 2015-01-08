#!/bin/bash

echo "Cleaning temp files..."
find . -name .DS_Store | xargs rm

echo "Finding all features..."
FEATURES=""
for i in `find corpus -depth 1`; do
    FEATURES="$FEATURES -f $i"
done
python feature_selection.py $FEATURES > all_features.pickle
echo "Preparing test data..."
python feature_selection.py -p test -f all_features.pickle > test.data
echo "TEST FILES" > test.filenames
ls test/ >> test.filenames

FEATURES=$(echo "$FEATURES" | sed -e 's/\-f/\-n/g')

rm -f results.txt
MODELS=`ls corpus`
#MODELS="paine jefferson"
for i in $MODELS; do
    ARGS=$(echo "$FEATURES" | sed -e "s/\-n corpus\/$i/\-p corpus\/$i/g")
    echo "Selecting features for $i with: $ARGS"
    python feature_selection.py $ARGS -f all_features.pickle > $i.data
    echo "Scaling $i"
    svm-scale -l 0 -s $i.data.range $i.data > $i.data.scale
    echo "Cross validation $i"
    cross_vars=$(./grid.py -svmtrain svm-train $i.data.scale | tail -n 1)
    c=$(echo $cross_vars | cut -f1 -d' ')
    g=$(echo $cross_vars | cut -f2 -d' ')
    rate=$(echo $cross_vars | cut -f3 -d' ')
    echo "$i best: c=$c g=$g rate=$rate" > $i.data.best
    echo "Training $i"
    svm-train -b 1 -c $c -g $g $i.data.scale $i.data.model > /dev/null
    echo "Scaling test data"
    svm-scale -l 0 -r $i.data.range test.data > test.data.scale
    echo "Predicting $i"
    svm-predict -b 1 test.data.scale $i.data.model $i.test.predict
    #cat $i.test.predict
    paste -d '\t' $i.test.predict test.filenames | tee $i.results
    echo -n "-r $i.results " >> results.txt
done
./format_results.py $(cat results.txt) > results.tsv

