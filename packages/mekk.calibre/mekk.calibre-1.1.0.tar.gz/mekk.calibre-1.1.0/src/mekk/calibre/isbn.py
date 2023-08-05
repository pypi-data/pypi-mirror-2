# -*- coding: utf-8 -*-

"""
ISBN extractint routine (and regexp)
"""

import re

############################################################
# Extracting ISBN from book text
############################################################

RE_ISBN = re.compile("(?:ISBN[ -]*(?:|10|13)|International Standard Book Number)[:\s]*(?:|, PDF ed.|, print ed.|\(pbk\)|\(electronic\))[:\s]*([-0-9Xx]{10,25})",
                     re.MULTILINE)


def look_for_isbn_in_text(text):
    """
    Scans text (string) for ISBN, returns one if found
    """
    isbns10 = []
    isbns13 = []
    for match in RE_ISBN.finditer(text):
        txt = match.group(1)
        txt = txt.replace("-", "")
        txt_len = len(txt)
        if txt_len == 10:
            isbns10.append(txt)
        elif txt_len == 13:
            isbns13.append(txt)
    # TODO: more sophisticated choice if there are many isbn's
    if isbns13:
        return isbns13[0]
    elif isbns10:
        return isbns10[0]
    else:
        return None
