import re,os,sys,traceback

""" tokenizer for Bavarian, Sturmibibl, stdin plain text """
for line in sys.stdin:

    # expect plain text format, insert/normalize spaces, keep other whitespaces
    line=line.strip()
    orig=line

    # break standard punctuation
    line=re.sub(r"([!\":,;/?])",r" \1 ",line)

    # undo EOL hyphens, break non-EOL -
    line=re.sub(r"([\-]) +(oder|und)",r"\\\1 \2",line)  # escape for reserved words
    line=re.sub(r"([a-zA-ZäöüßÄÖÜ])[\-] +([a-zA-ZäöüÄÖÜß])",r"\1\2",line) # unsplit
    line=re.sub(r"([^\\])\-",r" \1 ", line) # tokenize
    line=re.sub(r"\\([\-])",r"\1",line) # unescape

    # ., except with numbers or in Bible books
    line=re.sub(r"^b\.","b_",line)    # escape
    line=re.sub(r"([^0-9])\.(><[^0-9])",r"\1 . \2",line)
    line=re.sub(r"\.$",r" .",line)
    line=re.sub(r"\. ",r" . ",line)
    line=re.sub(r" \. ",r" . ",line)
    line=re.sub(r"^b_","b.",line) # unescape

    # expand *non-lengthening* apostrophe
    line=re.sub(r"([^a-zA-ZäöüÄÖÜß])'",r"\1 '", line)
    line=re.sub(r"'([A-Z])",r"' \1", line)

    # drop other formatting
    line=re.sub(r"\*([^\*]+)\*",r"\1",line)

    # some unclear typographical markers
    line="".join(line.split("+"))

    # drop additions
    line=re.sub(r"\([^\)\n]*\)","",line)    # optional content
    line=re.sub(r"\[[^\)\n]*\]","",line)    # footnotes

    # normalize whitespaces
    line=re.sub(r" +"," ",line)

#    print(orig)
    print(line)
#    print()
