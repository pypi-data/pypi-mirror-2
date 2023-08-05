# -*- coding: UTF-8 -*-
# vim: fileencoding=UTF-8 filetype=python ff=unix et ts=4 sw=4 sts=4 tw=120
#
# Copyright (c) 2010, Christer Sjöholm -- hcs AT furuvik DOT net
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''
    Utilities for working with file/dir/paths.

'''
from __future__ import absolute_import

import contextlib
import os
import re
import shutil
import tempfile
import time

from collections import namedtuple

DirectoryListing = namedtuple('DirectoryListing', 'dirs files')

def list_dir(path):
    ''' returns namedtuple DirectoryListing   (dirs, files)'''
    names = os.listdir(path)
    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(path, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
    return DirectoryListing(dirs, nondirs)

@contextlib.contextmanager
def tempdir(suffix='', prefix='tmp', dir_=None):
    '''context that creates and removes a temporary directory.

        >>> with tempdir() as tmpd:
        ...   os.path.isdir(tmpd)
        True
        >>> os.path.exists(tmpd)
        False
    '''
    tmpd = tempfile.mkdtemp(suffix, prefix, dir_)
    yield tmpd
    shutil.rmtree(tmpd)

def scan_for_new_files(path, interval=5, include=None, ignore=None):
    '''yields path of each file in the directory and then
    each new file that is added

    Arguments:
    - path -- directory to watch
    - interval -- number of seconds to delay between each scan
    - include -- If given, only file with names matching regexp is returned
    - ignore -- If given, files matching regexp is ignored

    filenames ending with .tmp is ignored
    '''
    include = include and re.compile(include)
    ignore = ignore and re.compile(ignore)
    previous_files = set()
    while True:
        current_files = list_dir(path).files
        for filename in current_files:
            #yield only files that was not there the last time we looked
            if filename in previous_files:
                continue
            if include and not include.match(filename):
                continue
            if ignore and ignore.match(filename):
                continue
            yield os.path.join(path, filename)
        previous_files = set(current_files)
        time.sleep(interval) # limit speed

