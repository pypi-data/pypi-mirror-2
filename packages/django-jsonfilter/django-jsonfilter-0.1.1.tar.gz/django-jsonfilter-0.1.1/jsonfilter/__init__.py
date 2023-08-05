#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read django-exported JSON data and output only objects of the specified
model type.
"""
# © Copyright 2010 Éric St-Jean, email: esj a-t w w d d-o-t c a
# 
# This file is part of django-jsonfilter.
# 
#     django-jsonfilter is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by the
#     Free Software Foundation, either version 3 of the License, or (at your
#     option) any later version.
# 
#     django-jsonfilter is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with django-jsonfilter.  If not, see <http://www.gnu.org/licenses/>.
from optparse import OptionParser
import re
import sys

MODEL_RE = (
    r"""(^\s*{                  # object opening re atom and json brackets
        [^{]*?"pk":[^\n\r]*?,   # PK field
        \s*"model":\ "%s",      # model name
        \s*"fields":\ {.*?}     # block of object fields
        \s*})                   # end of object curly and re atom close
        (?=,|\s*\])             # trailing comma or end-of-file closing ']'
    """          
)
RE_FLAGS = re.MULTILINE|re.DOTALL|re.VERBOSE

MODELNAME_RE = r'"model": "([^"]+)"'

class JSONModelFilter(object):
    
    def __init__(self, model):
        self.model = model

    def filter(self, stream=None):
        self.stream = stream
        return [r for r in self.filteriter(stream)]

    def filteriter(self, stream=None):
        if stream is not None:
            self.stream = stream
        self.result_iter = re.compile(
            MODEL_RE%self.model, RE_FLAGS
        ).finditer(self.stream.read())
        return self

    def __iter__(self):
        return self

    def next(self):
        return self.result_iter.next().group()
        
def list_models(stream):
    """Returns a list of model types found in json dump."""
    models = set()
    for m in re.compile(MODELNAME_RE).finditer(stream.read()):
        models.add(m.groups()[0])
    return sorted(list(models))
