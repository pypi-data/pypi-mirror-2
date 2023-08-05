# -*- coding: utf-8 -*-

"""
Scans given directory, adds to calibre all books which are not yet
present there. Duplicate checking is done solely on file content
comparison (file name may differ).  Used to double-check whether some
dir items were added to calibre, or not fully.

Example:

    python add_if_missing.py /home/jan/OldBooks

(and later remove OldBooks if everything is OK).

"""

import sys, os.path
from collections import defaultdict

from mekk.calibre.calibre_util import \
    find_calibre_file_names, add_to_calibre

from mekk.calibre.disk_util import \
    find_disk_files, file_size, are_files_identical

def run():
    if len(sys.argv) != 2:
        print "Execute with:"
        print "    calibre_add_if_missing  /some/dire/ctory/name"
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print "%s must be a directory"
        sys.exit(1)

    # size -> set of files with that size
    known_by_calibre = defaultdict(lambda: set())

    for f in find_calibre_file_names():
        known_by_calibre[ file_size(f) ].add( f )

    added_count = 0
    skipped_count = 0
    for f in find_disk_files(root):
        candidates = known_by_calibre[ file_size(f) ]
        if any( are_files_identical(f, c) for c in candidates ):
            print "Already present:", f
            skipped_count += 1
        else:
            print "Not registered by calibre:", f
            add_to_calibre(f)
            added_count += 1

    print
    print "%d files already present, %d added" % (skipped_count, added_count)
