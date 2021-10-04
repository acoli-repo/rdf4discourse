#!/bin/bash
MYHOME=`dirname $0`
SRC=https://bibeltext.com/bairisch/genesis/1.htm
TGT=html/`basename $(dirname $SRC)`/`basename $SRC`

# #
# # prep
# #########
# if [ ! -e anymalign ]; then
#   mkdir anymalign
#   wget -nc https://anymalign.limsi.fr/latest/anymalign2.5.zip -O anymalign/anymalign.zip
#   unzip -j anymalign/anymalign.zip -d anymalign
# fi;
## this extracts lexical correspondents, only, no full text alignment

# https://github.com/cisnlp/simalign: requires precomputed embeddings

# ##########
# # CONFIG #
# ##########
#
# # set to your "official" installation or get it from https://github.com/acoli-repo/conll-merge
# CONLL_MERGE=$HOME/conll;
#
# ########
# # INIT #
# ########
#
# # OS-specific representation of the CONLL_MERGE path (e.g., for cygwin)
# CONLL_MERGE_OS=$CONLL_MERGE;
# if echo $OSTYPE | grep -i cygwin >&/dev/null; then
# 	CONLL_MERGE_OS=`cygpath -wa $CONLL_MERGE_OS`;
# 	CONLL_MERGE_OS=`echo $CONLL_MERGE_OS | sed s/'\\\\'/'\\/'/g;`
# fi;
#
# # if $CONLL_MERGE/run.sh doesn't exist, build it
# MERGE=$CONLL_MERGE/cmd/merge.sh;
# if [ -x $MERGE ]; then
# 	echo using CONLL_MERGE installation at $CONLL_MERGE 1>&2;
# else
# 	wget -nc https://codeload.github.com/acoli-repo/conll/zip/master -O master.zip
# 	unzip master.zip
# 	mv conll-master $CONLL_MERGE;
# 	rm master.zip
# 	chmod u+x $CONLL_MERGE/cmd/*.sh;
# 	echo 1>&2;
# fi;

##############
# PROCESSING #
##############

if [ -s $MYHOME/bibl.tok ]; then
    echo found $MYHOME/bibl.tok, keeping it 1>&2
else

  if [ -s $MYHOME/bibl.tsv ]; then
    echo found $MYHOME/bibl.tsv, keeping it 1>&2
    cat $MYHOME/bibl.tsv
  else

    #
    # retrieve
    ############
    if [ -e $MYHOME/html ]; then
        echo found $MYHOME/html, skipping 1>&2
    else
      while [ ! -e $TGT ]; do
          if [ ! -e $MYHOME/html/`basename $(dirname $SRC)` ]; then
              mkdir -p $MYHOME/html/`basename $(dirname $SRC)`
          fi;
          SRC=`echo $SRC | sed s/'\/[^\.\/][^\.\/]*\/\.\.\/'/'\/'/g;`
          echo $SRC ">" $TGT 1>&2
          wget -nc $SRC -O $TGT
          SRC=`dirname $SRC`/`xmllint --html --recover --format $TGT --xpath "//a[text()='►']/@href[1]" | \
            sed -e s/'.*='//g -e s/'"'//g -e s/"'"//g`
            TGT=$MYHOME/html/`basename $(dirname $SRC)`/`basename $SRC`
      done
    fi

    #
    # process
    ###########

    books=`ls -tr $MYHOME/html` # exploits crawling order ;)
    for book in $books; do
        bid=`echo $book | \
          perl -pe '
          s/genesis/b.GEN/;
          s/exodus/b.EXO/;
          s/leviticus/b.LEV/;
          s/numbers/b.NUM/;
          s/deuteronomy/b.DEU/;
          s/joshua/b.JOS/;
          s/judges/b.JDG/;
          s/ruth/b.RUT/;
          s/1_samuel/b.1SA/;
          s/2_samuel/b.2SA/;
          s/1_kings/b.1KI/;
          s/2_kings/b.2KI/;
          s/1_chronicles/b.1CH/;
          s/2_chronicles/b.2CH/;
          s/ezra/b.EZR/;
          s/nehemiah/b.NEH/;
          s/esther/b.EST/;
          s/job/b.JOB/;
          s/psalms/b.PSA/;
          s/proverbs/b.PRO/;
          s/ecclesiastes/b.ECC/;
          s/songs/b.SON/;
          s/isaiah/b.ISA/;
          s/jeremiah/b.JER/;
          s/lamentations/b.LAM/;
          s/ezekiel/b.EZE/;
          s/daniel/b.DAN/;
          s/hosea/b.HOS/;
          s/joel/b.JOE/;
          s/amos/b.AMO/;
          s/obadiah/b.OBA/;
          s/jonah/b.JON/;
          s/micah/b.MIC/;
          s/nahum/b.NAH/;
          s/habakkuk/b.HAB/;
          s/zephaniah/b.ZEP/;
          s/haggai/b.HAG/;
          s/zechariah/b.ZEC/;
          s/malachi/b.MAL/;
          s/matthew/b.MAT/;
          s/mark/b.MAR/;
          s/luke/b.LUK/;
          s/acts/b.ACT/;
          s/romans/b.ROM/;
          s/1_corinthians/b.1CO/;
          s/2_corinthians/b.2CO/;
          s/galatians/b.GAL/;
          s/ephesians/b.EPH/;
          s/philippians/b.PHI/;
          s/colossians/b.COL/;
          s/1_thessalonians/b.1TH/;
          s/2_thessalonians/b.2TH/;
          s/1_timothy/b.1TI/;
          s/2_timothy/b.2TI/;
          s/titus/b.TIT/;
          s/philemon/b.PHM/;
          s/hebrews/b.HEB/;
          s/james/b.JAM/;
          s/1_peter/b.1PE/;
          s/2_peter/b.2PE/;
          s/1_john/b.1JO/;
          s/2_john/b.2JO/;
          s/3_john/b.3JO/;
          s/john/b.JOH/;  # replace after 1JO !!!
          s/jude/b.JUD/;
          s/revelation/b.REV/;'
        `
        chid=1
        while [ -e $MYHOME/html/$book/$chid.htm ]; do
            chap=$MYHOME/html/$book/$chid.htm
            xmllint --html --recover --format $chap | \
            perl -pe 's/\s+/ /g; s/(<div class="chap")/\n\1/g;' | \
            grep '<div class="chap"' | \
            perl -pe '
              s/(<span class="reftext")/\n\1/g;
              s/(<span class="maintext")/\t\1/g;
              s/<[^>\n\t]*>//g;
              s/<[^>\n\t]*//;
              s/[^<\n\t]*>//;
              s/([^\n]+\t)/'$bid.$chid.'$1/g;
              s/[\s^\n]*\t[\s^\n]*/\t/g;

              s/ *   De Bibl auf Bairisch[^\n]*//g;

              s/&auml;/ä/g;
              s/&Auml;/Ä/g;
              s/&ouml;/ö/g;
              s/&Ouml;/Ö/g;
              s/&szlig;/ß/g;
              s/&uuml;/ü/g;
              s/&Uuml;/Ü/g;

              ' | egrep '\.[0-9]+\.[0-9]+'
              chid=`echo 1+ $chid | bc`
        done
    done | cut -f 1,2 | tee $MYHOME/bibl.tsv
  fi | \
  \
  \
#
# tokenization
###
  python3 $MYHOME/bav_tokenize.py > $MYHOME/bibl.tok
fi;

#
# align => conll
##################
if [ ! -e $MYHOME/bibles ]; then
    svn checkout https://github.com/acoli-repo/acoli-corpora/trunk/biblical/data $MYHOME/bibles
fi

if [ ! -e $MYHOME/parallel ]; then
  mkdir $MYHOME/parallel
fi

# other language versions
bibles="
  bibles/germ/en_modern-english/web.xml
  bibles/indoeuropean-other/romance_italic/frn_french/french_lsg_utf8.xml
  bibles/indoeuropean-other/romance_italic/ita_italian/italian_diodati_1649_utf8.xml
  bibles/indoeuropean-other/romance_italic/spa_spanish/spanish_reina_valera_1909_utf8.xml
  bibles/indoeuropean-other/slavic/czc_czech/czech_bkr_utf8.xml
  bibles/germ/nld_dutch/Dutch.xml
  bibles/germ/deu_german/German.xml
  bibles/indoeuropean-other/romance_italic/por_portuguese/Portuguese.xml"
# NB: cat: https://web.archive.org/web/20080711105306/http://www.ibecat.org/biblia/

for bible in $bibles; do
  tgt=$MYHOME/parallel/`basename $(dirname $bible)`_`basename $bible`
  if [ -e $tgt ]; then
    echo found $tgt, keeping it 1>&2
  else
    echo bibl.tok + $bible '=>' $tgt 1>&2
    python3 $MYHOME/align-bibles.py $MYHOME/bibl.tok $bible -tok -low > $tgt
    echo 1>&2
  fi;
done

#
# discourse marker inference
#############################
if [ ! -e $MYHOME/discourse-markers ]; then
    svn checkout https://github.com/acoli-repo/rdf4discourse/trunk/discourse-markers $MYHOME/discourse-markers
# else
#     svn update $MYHOME/discourse-markers
fi

if [ ! -e $MYHOME/annotated ]; then
  mkdir $MYHOME/annotated
fi

for alignment in $MYHOME/parallel/*; do
  lang=""
  for l in en frn ita spa czc nld deu por; do
    if echo $alignment | grep '/'$l'_' >& /dev/null; then lang=$l; fi
  done

  if [ $lang = "deu" ]; then dimlex=DimLex.tsv; fi
  if [ $lang = "en" ]; then dimlex=pdtb2.tsv; fi
  if [ $lang = "frn" ]; then dimlex=lexconn.tsv; fi
  if [ $lang = "ita" ]; then dimlex=LICO-v.1.0.tsv; fi
  if [ $lang = "spa" ]; then dimlex=discmar.es.tsv; fi
  if [ $lang = "czc" ]; then dimlex=czedlex0.6.tsv; fi
  if [ $lang = "nld" ]; then dimlex=discodict.tsv; fi
  if [ $lang = "por" ]; then dimlex=LDM-v.1.3.tsv; fi

  if echo $dimlex | egrep . >&/dev/null; then
    tgt=$MYHOME/annotated/$lang.`basename $dimlex`.conll
    if [ -s $tgt ]; then
      echo found $tgt, skipping 1>&2
    else
      echo $alignment "+" $dimlex "=>" $tgt 1>&2
      python3 $MYHOME/parallel_gazetteer.py $alignment $MYHOME/discourse-markers/tsv/$dimlex -order 2 -word 3 > $tgt
    fi;

    if [ -s $tgt.slim ]; then
      echo found $tgt.slim, skipping 1>&2
    else
      echo $alignment "+" $dimlex "=>" $tgt.slim 1>&2
      python3 $MYHOME/parallel_gazetteer.py $alignment $MYHOME/discourse-markers/tsv/$dimlex -order 2 -word 3 -slim > $tgt.slim
    fi;

  fi;
done;

# merge
#########

## CoNLL-Merge implementation
# merged=$MYHOME/bibl.mrg.conll
# if [ -s $merged ]; then
#   echo found $merged, skipping 1>&2
# else
#   cat $MYHOME/bibl.tok | python3 $MYHOME/tsv2conll.py > $MYHOME/bibl.plain.conll
#   $MERGE $MYHOME/bibl.plain.conll $MYHOME/annotated/deu*slim 1 2 -lev -silent
# fi;

# Python implementation
merged=$MYHOME/bibl.mrg.conll
if [ -s $merged ]; then
  echo found $merged, skipping 1>&2
else
  tmp=$merged.tmp
  while [ -e $tmp ]; do
    tmp=$merged.`ls $merged* | wc -l`.tmp
  done;
  echo > $tmp
  echo $MYHOME/bibl.tok "=>" $merged 1>&2
  cat $MYHOME/bibl.tok | python3 $MYHOME/tsv2conll.py > $merged
  for anno in $MYHOME/annotated/*slim; do
    cp $merged $tmp
    echo $merged "+=" $anno 1>&2
    python3 $MYHOME/align.py 500 $tmp=1 $anno=1 | \
    perl -pe '
      s/([#][^\t]*)\t[\t \?\r]*\n/$1\n/;
      s/^[ \t\r]*\n/\n/;
    ' | egrep '^$|^[0-9]|^#' > $merged
  done
  rm $tmp
fi
