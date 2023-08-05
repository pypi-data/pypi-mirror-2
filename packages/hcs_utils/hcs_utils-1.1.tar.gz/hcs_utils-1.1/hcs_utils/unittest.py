#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: fileencoding=UTF-8 filetype=python ff=unix et ts=4 sw=4 sts=4 tw=120
# author: Christer Sjöholm -- hcs AT furuvik DOT net

from __future__ import absolute_import

import difflib
import json

def diff_str(str1, str2):
    return ''.join(difflib.ndiff(str1.splitlines(1), str2.splitlines(1)))

def eq_str(str1, str2, msg=None):
    """assert that strings str1 and str2 are equal.
    If msg is None result of difflib.ndiff() will be used.
    """
    assert str1 == str2, msg or diff_str(str(str1), str(str2))

def eq_json(obj1, obj2, msg=None):
    """assert that a and b have equal json representations.
    If msg is None, difflib.ndiff() will be used on json.
    """
    obj1 = json.dumps(obj1, indent=2)
    obj2 = json.dumps(obj2, indent=2)
    assert obj1 == obj2, msg or diff_str(obj1, obj2)
