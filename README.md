# discourse marker introduction

## idea

- given massively parallel text (e.g., bibles) and multilingual discourse marker inventories
- pick your target language, here, Bavarian
- for all translations with discourse marker inventories, annotate all senses of the longest matching discourse marker
- by alignment, project these to target language (`build.sh` => `build.mrg.conll`)
- use these projections as an ensemble to predict the most likely discourse relation for the target language (here: the suggested relation(s) that are least frequently rejected, `ensembly.py`, called by `eval.sh`)
- as we don't have target language annotations, evaluate against another projection (`eval.sh`)

## building

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
(cols 3 to 8 iterate for all other alignment pairs)

- ID: original token id (whitespace tokenization)
- WORD: original token
- TOK_ID: token id of normalized text
- NORM: normalized token, may split several WORD tokens
- LANG: translation language that the last two and the following three columns refer to
- PDTBx_SENSE: discourse relation(s), PDTB hierarchy depth x with x from 1 to 3

For every aligned translation, the columns WORD TOK_ID, NORM, LANG and PDTB1..3 are repeated.
For the current setup, the aligned languages are

- Czech (cols 6-8)
- German (cols 12-14)
- English (cols 18-20)
- French (cols 24-26)
- Italian (cols 30-32)
- Dutch (cols 36-38)
- Portuguese (cols 42-44)
- Spanish (cols 48-50)

In the annotation columns, `_` means that alignment was successful but that no discourse information could be confirmed. `?` means that no target language alignment could be established.

For evaluation, run

    $> bash -e ./eval.sh

## notes

cf. http://www.semantic-web-journal.net/system/files/swj2898.pdf, also for related research

they demonstrate robustness of discourse annotations across (a certain sample) of languages

a difference is that we are completely annotation-free
