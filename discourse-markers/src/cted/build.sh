#!/bin/bash
# retrieve C-TED content

if [ ! -e data ]; then
  svn checkout "https://github.com/tjunlp-lab/Shallow-Discourse-Annotation-for-Chinese-TED-Talks/trunk/Dataset for Shallow Discourse Annotation for Chinese TED Talks Accepted by LREC2020/" data
fi;

# frequency table
for ann in data/Ann*/tokens/*.txt; do
  raw=`echo $ann | sed s/'Ann'/'Raw'/`;
  if [ -e $raw ]; then
    python3 extract-cues.py $raw $ann
  fi;
done | egrep -a '[a-zA-Z]' | sort | uniq -c | sed -e s/'^  *'// -e s/'  *'/'\t'/g | \
python3 tsv2dimlex.py > cted.xml
