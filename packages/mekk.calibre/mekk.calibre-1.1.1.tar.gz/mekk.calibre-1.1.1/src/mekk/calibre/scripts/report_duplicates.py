# -*- coding: utf-8 -*-

"""
Analyzes calibre database and reports possible duplicates (detected
using both actual books, and author/title matching). Prints the
report. Do not perform any changes, the report can be used to decide
which books to merge using Calibre interface.

With `--html` prints report as HTML.

Example:

    calibre_report_duplicates

or

    calibre_report_duplicates --html > report.html
    firefox report.html

"""

import sys
from collections import defaultdict
from optparse import OptionParser
import difflib

from mekk.calibre.calibre_util import \
    find_calibre_books

from mekk.calibre.disk_util import \
    file_size, are_files_identical, file_extension

# Expected similarity ratio for difflib.get_close_matches. Default 0.6
# is a little bit too small
EXPECTED_AUTHOR_SIMILARITY = 0.75
EXPECTED_TITLE_SIMILARITY = 0.65


class Report(object):

    def start(self):
        self.items = []
        self.begin()

    def note_book_pair(self, book1, book2):
        observations = []
        merge_safe = True

        for author1 in book1.authors:
            for author2 in difflib.get_close_matches(
                author1, book2.authors,
                cutoff=EXPECTED_AUTHOR_SIMILARITY):
                if author1 == author2:
                    observations.append(u"Identical author %s" % author1)
                else:
                    observations.append(u"Similar authors %s and %s" % (
                            author1, author2))

        if book1.title == book2.title:
            observations.append("Identical title")
        elif difflib.get_close_matches(book1.title, [book2.title],
                                       cutoff=EXPECTED_TITLE_SIMILARITY):
            observations.append("Similar titles")

        files1 = dict((file_extension(name), name) for name in book1.files)
        files2 = dict((file_extension(name), name) for name in book2.files)
        all_exts = set(files1.keys() + files2.keys())

        for ext in all_exts:
            name1 = files1.get(ext)
            name2 = files2.get(ext)
            if name1 is None:
                observations.append("%s only in second book" % ext)
            elif name2 is None:
                observations.append("%s only in first book" % ext)
            else:
                size = file_size(name1)
                if size == file_size(name2) \
                        and are_files_identical(name1, name2):
                    observations.append(
                        "%s formats are identical (size %d)" % (
                            ext, size))
                else:
                    observations.append(
                        "%s formats DIFFERENT (size %d - %d)" % (
                            ext, size, file_size(name2)))
                    merge_safe = False

        #self.item(book1, book2, observations, merge_safe)
        self.items.append((book1, book2, observations, merge_safe))

    def stop(self):
        self.items.sort(key=lambda (b1, b2, obs, safe): \
                            (not safe, sorted(b1.authors + b2.authors),
                             b1.title, b2.title, b1.id, b2.id))
        for item in self.items:
            self.item(*item)
        self.end()


class TextReport(Report):

    def begin(self):
        pass

    def item(self, book1, book2, observations, merge_safe):
        print "-" * 70
        print ("| %-10s | %-30s | %-30s |" % (
                book1.id, book1.title.strip()[:30],
                ", ".join(a.strip() for a in book1.authors)[:30])).encode("utf-8")
        print ("| %-10s | %-30s | %-30s |" % (
                book2.id, book2.title.strip()[:30],
                ", ".join(a.strip() for a in book2.authors)[:30])).encode("utf-8")
        for obs in observations:
            print "|", obs.encode("utf-8")
        print "|", merge_safe and "Merging books should be safe" \
                               or "Merging books may loose data"
        print "-" * 70
        print

    def end(self):
        pass


class HTMLReport(Report):

    def begin(self):
        self.cls = "odd"
        print """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Calibre duplicates</title>
    <style type="text/css">
.safe-odd {
  background-color: #CFC;
}
.safe-even {
  background-color: #ADA;
}
.unsafe-odd {
  background-color: #FCC;
}
.unsafe-even {
  background-color: #DAA;
}
tr.first td {
  padding: 10px 2px 2px 2px;
}
tr.internal td {
  padding: 2px;
}
tr.last td {
  padding: 2px 2px 10px 2px;
}
    </style>
  </head>
<body>
<table cellspacing="0">
"""

    def item(self, book1, book2, observations, merge_safe):
        cls = self.cls
        self.cls = cls == "odd" and "even" or "odd"
        if merge_safe:
            cls = "safe-" + cls
        else:
            cls = "unsafe-" + cls

        leftcol_items = [book1.id, book1.title] + book1.authors
        rightcol_items = [book2.id, book2.title] + book2.authors
        observations.append(
            merge_safe and "Book merge is safe" or "Book merge can loose data")

        rows = map(
            lambda l, c, r: (l or "", c or "", r or ""),
            leftcol_items, observations, rightcol_items)

        print (u"""<tr class="%s first"><td>%s</td><td>%s</td><td>%s</td></tr>""" % (
            (cls,) + rows[0])).encode("utf-8")
        for i in range(1, len(rows)-1):
            print (u"""<tr class="%s internal"><td>%s</td><td>%s</td><td>%s</td></tr>""" % (
                (cls,) + rows[i])).encode("utf-8")
        print (u"""<tr class="%s last"><td>%s</td><td>%s</td><td>%s</td></tr>""" % (
            (cls,) + rows[-1])).encode("utf-8")

    def end(self):
        print """
</table>
</body>
</html>"""


def process_options():
    parser = OptionParser()
    parser.add_option("-m", "--html",
                      action="store_true", dest="html", default=False,
                      help="Output result as HTML")
    (options, args) = parser.parse_args()
    if args:
        print "Execute with:"
        print "    calibre_report_duplicates"
        print "or"
        print "    calibre_report_duplicates --html"
        sys.exit(1)
    return options


def run():
    """
    Run calibre_report_duplicates
    """
    options = process_options()

    report = options.html and HTMLReport() or TextReport()

    # (binary dupes detection helper) Mapping
    #     size -> [  (filename, book), (filename, book), ... ]
    # where filename points actual file of this size, and book is full
    # book info (id, uuid, title, isbn, files)
    books_of_size = defaultdict(lambda: [])

    # (author/title dupes detection helper) Mapping
    #     author -> [ book, book, ... ]
    books_by_author = defaultdict(lambda: [])

    # id -> book
    books_by_id = dict()

    print >> sys.stderr, "Loading books info..."

    for book in find_calibre_books():
        books_by_id[book.id] = book
        for file_name in book.files:
            size = file_size(file_name)
            books_of_size[size].append((file_name, book))
        for author in book.authors:
            books_by_author[author].append(book)

    print >> sys.stderr, "... book list loaded"

    likely_identical = set()  # pary id

    print >> sys.stderr, "Looking for identical files..."

    for size, items in books_of_size.iteritems():
        if len(items) <= 1:
            continue
        for first_idx in range(0, len(items)-1):
            first_file, first_book = items[first_idx]
            for second_idx in range(first_idx + 1, len(items)):
                second_file, second_book = items[second_idx]
                if are_files_identical(first_file, second_file):
                    likely_identical.add((min(first_book.id, second_book.id),
                                          max(first_book.id, second_book.id)))

    identical_count = len(likely_identical)
    print >> sys.stderr, "... analyzed, %d possible pairs found" % identical_count

    print >> sys.stderr, "Looking for matching authors and titles..."

    all_authors = books_by_author.keys()

    for author, books in books_by_author.iteritems():
        # Adding other similar authors to the competition
        similar_authors = difflib.get_close_matches(
            author, all_authors, n=5, cutoff=EXPECTED_AUTHOR_SIMILARITY)
        if len(similar_authors) > 1:
            # Note: "current" books are also here as author is similar to self
            books = sum((books_by_author[author_name]
                         for author_name in similar_authors), [])
            # duplicate pruning (book can have many authors)
            books = [books_by_id[id]
                     for id in set(book.id for book in books)]
        if len(books) <= 1:
            continue

        # Looking for similar titles
        all_titles = [book.title for book in books]
        for base_book in books:
            similar_titles = difflib.get_close_matches(
                base_book.title, all_titles,
                n=5, cutoff=EXPECTED_TITLE_SIMILARITY)
            if len(similar_titles) <= 1:
                continue
            similar_books = [book
                             for book in books
                             if book.title in similar_titles]
            for idx1 in range(0, len(similar_books)-1):
                book1 = similar_books[idx1]
                for idx2 in range(idx1 + 1, len(similar_books)):
                    book2 = similar_books[idx2]
                    likely_identical.add((min(book1.id, book2.id),
                                          max(book1.id, book2.id)))

    print >> sys.stderr, "... analyzed, %d new pairs found" % (
        len(likely_identical) - identical_count)

    print >> sys.stderr, "Generating report."

    report.start()

    for b1, b2 in likely_identical:
        report.note_book_pair(books_by_id[b1], books_by_id[b2])

    report.stop()
