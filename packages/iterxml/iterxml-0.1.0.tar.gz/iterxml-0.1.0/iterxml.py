# -*- coding: utf-8 -*-
#
#  iterxml.py
#  iterxml
# 
#  Created by Lars Yencken on 13-07-2010.
#  Copyright 2010 Lars Yencken. All rights reserved.
#


"""
A library for iterating through large xml files.
"""

from xml.etree import cElementTree as ElementTree
import bz2
import gzip

def iterxml(stream_or_file, tag_of_interest):
    """
    When passed a stream or filename and a tag of interest, returns an
    iterator over matching nodes in the stream. If a filename is given with
    standard gzip or bz2 file extensions, the file is transparently
    decompressed.
    
    The iteration destructively removes node history after each element is
    parsed, in order to allow parsing of files whose contents are too large
    to fit into memory.
    """
    if isinstance(stream_or_file, (str, unicode)):
        if stream_or_file.endswith('.bz2'):
            istream = bz2.BZ2File(stream_or_file, 'r')
        elif stream_or_file.endswith('.gz'):
            istream = gzip.GzipFile(stream_or_file, 'r')
        else:
            istream = open(stream_or_file, 'r')
    else:
        istream = stream_or_file

    context = iter(ElementTree.iterparse(istream, events=('start', 'end')))
    event, root = context.next()
    root = root

    for event, node in context:
        if event == 'end' and node.tag == tag_of_interest:
            yield node
            root.clear()

# vim: ts=4 sw=4 sts=4 et tw=78:
