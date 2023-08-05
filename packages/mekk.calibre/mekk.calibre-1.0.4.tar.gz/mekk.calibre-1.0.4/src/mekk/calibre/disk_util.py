# -*- coding: utf-8 -*-

import os.path, os, filecmp

def find_disk_files(root,
                    ignored_names = ["metadata.db"],
                    ignored_extensions = [".jpg", ".gif"]):
    """
    Locates and returns all disk files under directory root, ignoring
    those unnecessary.
    """
    files = []
    def grab_file(arg, dirname, fnames):
        for short_name in fnames:
            full_name = os.path.join(dirname, short_name)
            if os.path.isfile(full_name):
                if short_name in ignored_names:
                    continue
                if any( short_name.endswith(ext) for ext in ignored_extensions ):
                    continue
                files.append(full_name)
    os.path.walk(root, grab_file, None)
    return files

def file_size(filename):
    s = os.stat(filename)
    return s.st_size

def file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()

def are_files_identical(filename1, filename2):
    return filecmp.cmp(filename1, filename2, False)

