#!/bin/bash
echo "synopsis: "$0" CORPUS LANG1 LANG2  [-invert] [MODE]
CORPUS OPUS corpus id, e.g., Europarl (check its existence under http://opus.lingfil.uu.se/Europarl/, etc.)
	currently: Books, DGT, DOGC, ECB, EMEA, EUbookshop, EUconst, Europarl3, Europarl, GNOME, GlobalVoices,
	hrenWaC, JRC-Acquis, KDE4, KDEdoc, MBS, MultiUN, News-Commentary, News-Commentary11, OpenOffice,
	OpenOffice3, OpenSubtitles, OpenSubtitles2012, OpenSubtitles2013, OpenSubtitles2016, ParCor, PHP,
	SETIMES2, SPC, Tatoeba, TEP, TedTalks, TED2013, Tanzil, Ubuntu, UN, WikiSource, Wikipedia, WMT-News
LANGi  OPUS language id, e.g., de, en, it, currently:
	ace, ady, af, ain, ak, sq, am, ara, ar_SY, ar, ar_TN, an, hy, as, ast, aym, az_IR, az, bal, ba, eu_ES, eu,
	be, bem, bn_IN, bn, ber, bho, byn, nb_NO, nb, bs, br, bg, bg_BG, bua, my, ca, cat, ceb, km, ch, ce, chr,
	ny, zh_cn, zh_tw, zh_en, zh, zh_TW, zh_CN, zh_zh, zh_HK, cv, kw, co, mus, crh, hr, cs, da_DK, da, dv, nl_NL,
	nl_BE, nl, dz, en_ZA, en, en_CA, en_AU, en_NZ, en_GB, en_US, ang, eo, et, ee, fo, fil, fi, fr, fr_FR, fr_BE,
	fr_CA, frm, fur, ff, gd, gl, lg, ka, de_AT, de_DE, de, de_CH, el, grc, gn, gu, ht, ha, haw, he, hil, him,
	hi_IN, hi, hu, is, io, ig, id, inh, ia, ie, iu, ga, it_IT, it, jp, ja, jv, kbd, kab, kl, xal, kn, kr, ks,
	csb, kk, rw, ky, tlh, kg, kok, ko, ku, lad, lo, la, lv, li, ln, lt, jbo, nds, dsb, luo, lb, mk, mai, mg, ms,
	ms_MY, ml, mt, gv, mi, arn, mr, mh, mn, nqo, nah, nr, nap, ne, non, se, no, no_nb, nn_NO, nn, oc, oj, or,
	om, os, pam, pa, pap, nso, fa, fa_IR, fa_AF, pl, pt, pt_PT, pt_BR, pt_br, ps, qu, ro, rm, rom, ru, sm, sa,
	sc, sco, sr, sr_ME, shn, sn, scn, sd, si, sk, sl, so, son, st, es_PR, es_HN, es_VE, es, es_EC, es_CO, es_GT,
	es_ES, es_UY, es_SV, es_NI, es_MX, es_PE, es_PA, es_DO, es_CL, es_CR, es_AR, su, sw, sv, syr, tl, tl_PH, ty,
	tg_TJ, tg, ta_LK, ta, tt, te, tet, th, bod, bo, ti, tpi, ts, tr, tr_TR, tk, udm, ug, uk, hsb, ur_PK, ur, uz,
	ve, vi, vi_VN, vo, wa, cy, fy, wo, xh, yi, yo, zza, zu, acm, arq, ary, arz, avk, brx, ckb, ckt, cmn, cn, cycl,
	foo, frp, gr, guc, hne, hrx, ic, ksh, lij, lld, ltg, lzh, mhr, miq, mo, nan, nhn, nov, npi, orv, pcd, pes, 
	pms, pmy, pnb, po, prg, quz, qya, scc, scr, sh, shs, sjn, sml, swh, szl, tc, tmp, toki, tpw, trv, vec, wae,
	wuu, yue, ze_en, ze_zh, zhs, zht, zsm
-invert reverse direction of alignment
MODE mode of the MOSES factored alignment: grow-diag-final-and (DEFAULT), grow, intersect, srctotgt, tgttosrc
given an OPUS MOSES alignment, create a CoNLL view
" 1>&2;

if echo $4 $5 | egrep -i '\-invert' >& /dev/null; then
	invert="-invert";
fi;

mode=`echo $4 $5 | sed s/' *\-invert *'//g;`
if echo $mode | grep '^$'; then mode=grow-diag-final-and; fi;

src=http://opus.lingfil.uu.se/$1/wordalign/$2-$3/c.true.$2.gz;
tgt=http://opus.lingfil.uu.se/$1/wordalign/$2-$3/c.true.$3.gz;
model=http://opus.lingfil.uu.se/$1/wordalign/$2-$3/model/aligned.$mode.gz;
	#aligned.grow-diag-final-and.gz is too noisy

echo Moses2CoNLL $model $src $tgt $invert 1>&2;
if javac Moses2CoNLL.java; then java Moses2CoNLL $model $src $tgt $invert -silent; fi;