# -*- coding: utf-8 -*-

import re

############################################################
# Extracting ISBN from book text
############################################################

re_isbn = re.compile("(?:ISBN[ -]*(?:|10|13)|International Standard Book Number)[:\s]*(?:|, PDF ed.|, print ed.|\(pbk\)|\(electronic\))[:\s]*([-0-9Xx]{10,25})", re.MULTILINE)

def look_for_isbn_in_text(text):
    """
    Scans text (string) for ISBN, returns one if found
    """
    isbns10 = []
    isbns13 = []
    for m in re_isbn.finditer(text):
        txt = m.group(1)
        txt = txt.replace("-", "")
        l = len(txt)
        if l == 10:
            isbns10.append(txt)
        elif l == 13:
            isbns13.append(txt)
    if isbns13:
        return isbns13[0]   # TODO: more sophisticated choice if there are many isbn's
    elif isbns10:
        return isbns10[0]
    else:
        return None

