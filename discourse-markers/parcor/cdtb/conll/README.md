# CoNLL version of the CDTB discourse annotations

- discourse and syntax only (no coref, no uninterpretables
- removed files without annotation

	$> rm `for file in */*; do echo -n $file' '; cut -f 8- $file | grep '_' | cut -f 1 | grep -v '_' | wc -l; done | grep ' 0' | sed s/' 0$'//`

Note that these are just 54 files, with one single English file. This cannot be the original data.
But these are not the same files, so, these amount to really 54 different files per language.

Overall, these are 1155 discourse relations (da 577, en 22, it 556)
