#!/usr/bin/env python
"""Read django-exported JSON data and output only objects of the specified
model type.
"""
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
        

