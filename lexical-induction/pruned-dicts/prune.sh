#!/bin/bash

# this is a subset of the ACoLi Dict Graph
# in pruning, we remove every bidictionary for which no non-cyclical path exists that connects it with a discourse marker inventory

for lang in \
	ur hi ms cy sq hw vi zlm id bs hu ko lt rom tt be	\
	fa th ta sk ar mt nn nb se lv et sr tl ast wo br sa gd szl rh crh; do
	for file in `find | egrep -i '[^a-z]'$lang'[^a-z]'`; do
		rm $file;
	done
done;
	