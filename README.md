# discourse marker introduction

## howto

run

    $> bash -e ./build.sh

creates `build.mrg.conll`, with

    # b.GEN.1.2
    # Und d Erdn war oed und laer , finster war s über dyr Teuffn , und yn n Herrgot sein Geist gschwöbt über n Wasser .
    1	Und	1	und	?	?	?	?	1	und	de	COMPARISON|EXPANSION|TEMPORAL	COMPARISON:Contrast|EXPANSION:Conjunction|TEMPORAL:Asynchronous	COMPARISON:Contrast|EXPANSION:Conjunction|TEMPORAL:Asynchronous:Precedence	1	und	?	?	?	?	1	und	?	?	?	?	1	und	it	EXPANSION|TEMPORAL	EXPANSION:Conjunction|TEMPORAL:Asynchronous	EXPANSION:Conjunction|TEMPORAL:Asynchronous:Precedence	1	und	?	?	?	?	1	und	?	?	?	?	1	und	_	_	_	_
    2	d	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_	2	d	_	_	_	_

Columns:

- 1 ID
- 2 WORD
- 3 TOK_ID
- 4 NORM
- 5 LANG
- 6 PDTB1_SENSE
- 7 PDTB2_SENSE
- 8 PDTB3_SENSE
- 5 TOK_ID
- 6 LANG
- 7 PDTB1_SENSE
- 8 PDTB2_SENSE
- 9 PDTB3_SENSE
etc.

- ID: original token id (whitespace tokenization)
- WORD: original token
- TOK_ID: token id of normalized text
- NORM: normalized token, may split several WORD tokens
- LANG: translation language that the last two and the following three columns refer to
- PDTBx_SENSE: discourse relation(s), PDTB hierarchy depth x with x from 1 to 3

For every aligned translation, the columns WORD TOK_ID, NORM, LANG and PDTB1..3 are repeated.

In the annotation columns, `_` means that alignment was successful but that no discourse information could be confirmed. `?` means that no target language alignment could be established.

For evaluation, run

    $> bash -e ./eval.sh

## notes

cf. http://www.semantic-web-journal.net/system/files/swj2898.pdf, also for related research

they demonstrate robustness of discourse annotations across (a certain sample) of languages

a difference is that we are completely annotation-free
