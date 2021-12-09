#!/bin/bash



for dict in $*; do
	echo -n $dict' ';
	lang $dict
done