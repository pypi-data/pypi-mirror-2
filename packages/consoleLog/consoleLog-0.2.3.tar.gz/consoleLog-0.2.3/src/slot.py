# -*- coding: utf-8 -*-
#
#  slot.py
#  consoleLog
# 
#  Created by Lars Yencken on 03-05-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#

"""
"""

import sys

import shellColor

class Slot(object):
    """
    A generic text slot which can be overwritten repeatedly.
    """
    def __init__(self, text=u'', stream=sys.stdout):
        if u'\n' in text:
            raise Exception('slots cannot undo newlines')
        self.stream = stream
        self.last_text = None
        self.is_finished = False
        if text:
            self.update(text)

    def update(self, text):
        if self.is_finished:
            raise Exception("slot already finalized, cannot update it")

        if isinstance(text, unicode):
            text = text.encode('utf8')

        if self.last_text:
            last_len = shellColor.realLen(self.last_text)
            self.stream.write('\b' * shellColor.realLen(self.last_text))
            this_len = shellColor.realLen(text)
            if this_len < last_len:
                text = text + ' ' * (last_len - this_len)

        self.stream.write(text)
        self.stream.flush()
        self.last_text = text

    def finish(self, text=None):
        if text:
            self.update(text)
        print >> self.stream
        self.is_finished = True

# vim: ts=4 sw=4 sts=4 et tw=78:
