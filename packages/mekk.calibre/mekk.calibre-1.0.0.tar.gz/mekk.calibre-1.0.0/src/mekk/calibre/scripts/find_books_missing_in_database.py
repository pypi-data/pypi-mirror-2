# -*- coding: utf-8 -*-

"""
Looking up files which are present on disk, but are
missing in Calibre database (inconsistencies).

The files are reported to standard output. To add them
all to calibre, pipe output. For example:

 python find_books_missing_in_database.py | xargs -d "\n" calibredb add

(but, better, review everything beforehand)
"""

#import os.path
#import subprocess
#from lxml import objectify
#from StringIO import StringIO
#import sys

from mekk.calibre.calibre_util import find_calibre_file_names
from mekk.calibre.disk_util import find_disk_files
import os.path

############################################################
# Main
############################################################

def run():
    known_by_calibre = set()

    for f in find_calibre_file_names():
        known_by_calibre.add(f)

    root = os.path.dirname(os.path.dirname(os.path.dirname(f)))

    correct_count = 0
    missing_count = 0
    for f in find_disk_files(root):
        if not f in known_by_calibre:
            print f
            missing_count += 1
        else:
            correct_count += 1

    print >> sys.stderr, "%d files properly registered in calibre" % correct_count
    if missing_count:
        print >> sys.stderr, "%d files unknown" % missing_count
