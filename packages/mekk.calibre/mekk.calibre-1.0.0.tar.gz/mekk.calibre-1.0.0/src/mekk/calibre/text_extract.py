# -*- coding: utf-8 -*-

"""
Text extraction routines
"""

# TODO: differentiate partial and full extract (and handle the latter too)

import subprocess, os

from mekk.calibre.disk_util import file_extension

from lxml import etree, html

from mekk.calibre.config import standard_config
config = standard_config()

############################################################
# Extracting leading pages of the book from different
# formats
############################################################

text_extractors = dict()

def grab_file_text_pdf(file_path):
    txt = subprocess.Popen(
        [ config.pdftotext, file_path, 
          "-f", "1", "-l", str(config.guess_lead_pages), "-"],
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, 'w'),
        ).communicate()[0]
    return txt

if config.pdftotext:
    text_extractors[".pdf"] = grab_file_text_pdf

def grab_file_text_txt(file_path):
    f = open(file_path, "r")
    txt = "".join( f.readlines(config.guess_lead_lines) )
    return txt

text_extractors[".txt"] = grab_file_text_txt

def grab_file_text_catdoc(file_path):
    txt = subprocess.Popen(
        [ config.catdoc, file_path ],
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, 'w'),
        ).communicate()[0]
    return txt

if config.catdoc:
    text_extractors[".rtf"] = grab_file_text_catdoc
    text_extractors[".doc"] = grab_file_text_catdoc

def grab_file_text_djvu(file_path):
    txt = subprocess.Popen(
        [ config.djvutxt, "-page=0-%d" % config.guess_lead_pages, file_path ],
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, 'w'),
        ).communicate()[0]            
    return txt

if config.djvutxt:
    text_extractors[".djvu"] = grab_file_text_djvu

def grab_file_text_chm(file_path):
    pipe = subprocess.Popen(
        [ config.archmage, "--dump", file_path ],
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, 'w'),
        )
    lines = []
    for line in pipe.stdout:
        if line.strip():
            lines.append(line)
            if len(lines) > config.guess_lead_lines:
                break
    pipe.terminate()
    doc_text = "".join(lines)
    try:
        return "\n".join( html.fromstring( doc_text ).itertext() ).encode("utf-8")
    except etree.XMLSyntaxError:
        print "Problems parsing content of", file_path
        return doc_text.encode("utf-8")

if config.archmage:
    text_extractors[".chm"] = grab_file_text_chm

############################################################
# Wrapper for extractor routines
############################################################

def grab_file_text_for_analysis(file_path):
    """
    Grabs a couple of leading pages from given file, returns them as text
    """
    format = file_extension(file_path)

    routine = text_extractors.get(format)

    if routine:
        return routine(file_path)
    else:
        raise Exception("Unknown format: %s" % format)
    return txt

def can_extract_text_from(file_path):
    """
    Preliminary (extension-based) test whether given file can work
    """
    return file_extension(file_path) in text_extractors
    
