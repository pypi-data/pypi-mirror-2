# -*- coding: utf-8 -*-

"""
Wrappery dla komend wykonywanych na Calibre
"""

import os.path
import subprocess
from lxml import objectify
from StringIO import StringIO
import sys
from collections import namedtuple
from tempfile import NamedTemporaryFile

from mekk.calibre.config import standard_config
config = standard_config()

############################################################
# Internal helpers
############################################################

def calibre_query_files(search = None):
    """
    Iterates over calibre database, yielding item for each file.
    Starts from newest, apply search criteria if given
    """
    # http://calibre-ebook.com/user_manual/cli/calibredb.html#calibredb-catalog
    options = []
    if search:
        options.extend(["--search", search])
    #if sort_by:
    #    options.extend(["--sort-by", sort_by])
    options.extend(["--sort-by", "id"])

    cat_file = NamedTemporaryFile(suffix = ".xml", delete = False)
    cat_file.close()
    try:
        subprocess.check_call(
            [config.calibredb, "catalog", cat_file.name] + options)
        tree = objectify.parse(open(cat_file.name))
        root = tree.getroot()
        return root.iterchildren(reversed = True)
    except OSError, e:
        if e.errno == 2:
            raise Exception("calibredb (configured as %s) not found. Install Calibre, or edit %s to set proper path to it." % (config.calibredb, CONFIG_LOCATION))
        else:
            raise
    finally:
        os.remove(cat_file.name)

############################################################
# Public interface - general functions
############################################################

def find_calibre_file_names():
    """
    Yields all files registered in Calibre database (just filenames)
    """
    for el in calibre_query_files():
        try:
            files = [ fmtel.text 
                      for fmtel in el.formats.iterchildren("format") ]
            for f in files:
                yield f
        except AttributeError:
            print >> sys.stderr, "Warning: book %s (%s) has no file associated." % (el.id.text, el.title.text)

FileItem = namedtuple('FileItem', 'id uuid title isbn files')

def find_calibre_books(search = None):
    """
    Yields all books (or all books matching given search, if specified)

    Routine yields objects with fields:
       id, 
       uuid, 
       title,
       isbn,   # can be None
       files  (list of all book formats/files)
    """
    checked_count = 0
    for item_no, el in enumerate( calibre_query_files(search) ):
        if hasattr(el, "isbn"):
            isbn = el.isbn.text
        else:
            isbn = None
        try:
            files = [ fmtel.text 
                      for fmtel in el.formats.iterchildren("format") ]
        except AttributeError:
            files = []
            print "Warning: book %s (%s) has no file associated." % (el.id.text, el.title.text)
            
        yield FileItem(id = el.id.text,
                       uuid = el.uuid.text,
                       title = el.title.text,
                       isbn = isbn,
                       files = files)

def add_to_calibre(filename):
    """
    Add new book to calibre. filename is a file containing the book (which lies outside
    calibre directory and will be copied).
    """
    print "Importing", filename
    subprocess.check_call(
        [config.calibredb, "add", filename])
    print " ... imported"

def add_format_to_calibre(item_id, filename):
    """
    Add new format to existing book. item_id is a calibre book identifier,
    filename is a file containing the new "format" (which lies outside
    calibre directory and will be copied).
    """
    print " ... importing %s as new format for item %s" % (filename, item_id)
    subprocess.check_call(
        [config.calibredb, "add_format", item_id, rtf_name])
    print " ... imported"

############################################################
# Public interface - specific-task functions
############################################################

def save_isbn(item, isbn):
    print "Saving isbn %s to book %s" % (isbn, item)
    opf = subprocess.Popen(
        [config.calibredb, "show_metadata", item.id, "--as-opf"],
        stdout=subprocess.PIPE).communicate()[0]
    opf = opf.replace("</metadata>",
                """<dc:identifier opf:scheme="ISBN">%s</dc:identifier></metadata>""" % isbn)
    opf_file = NamedTemporaryFile(suffix = ".opf", delete = False)
    opf_file.write(opf)
    opf_file.close()
    subprocess.check_call(
        [config.calibredb, "set_metadata", item.id, opf_file.name])
    os.remove(opf_file.name)

