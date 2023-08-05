"""
The sole purpose of this module to provide easy to remember way of downloading
files with out-of-the-box Python installation:

    python -m wget <URL>


This module should probably be renamed to something else before incorporated
into Python library to avoid complains about missing options, but it is hard
to invent something more intuitive (like 'fetch').
"""

import sys, urllib, shutil, os, urlparse
import tempfile
import math


version = "0.4"


def filename_from_url(url):
    """:return: detected filename or None"""
    fname = os.path.basename(urlparse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname


def get_console_width():
    """
    http://bugs.python.org/issue8408
    """
    return 80

def progress_callback(blocks, block_size, total_size):
    """callback function for urlretrieve that is called when connection is
    created and when once for each block

    draws progress bar (one of free depending on available console wydth:
    [..  ] downloaded / total
    downloaded / total
    [.. ]

    do not display anything if there is not much space on the screen.
    show bytes counter if total_size is unknown as many bytes as possible.

    use sys.stdout.write() instead of "print,", because it allows one more
    symbol at the line end without linefeed on Windows

    :param blocks: number of blocks transferred so far
    :param block_size: in bytes
    :param total_size: in bytes, can be -1 if server doesn't return it
    """
    width = get_console_width()
    size_width = len("%s" % total_size)
    size_field_width = size_width*2 + 3 # 'xxxx / yyyy'
    min_bar_width = 3 # [.]


    # process special case and return immediately
    if total_size <= 0:
        msg = "\r%s / unknown" % (blocks * block_size)
        if width-1 > 0:
            sys.stdout.write(msg[:width-1]) # leave one character to avoid linefeed
        return


    total_blocks = math.ceil(float(total_size) / block_size)

    # if we need to draw bar
    full_info = (width >= min_bar_width+1+size_field_width+1)
    #                              trailing +1 to avoid linefeed when printing
    size_only = (not full_info and width > size_field_width)
    bar_only = (not size_only and width > min_bar_width)

    # drawing bar
    if full_info:
        bar_width = width-1-size_field_width-1
    elif bar_only:
        bar_width = width-1
   
    if full_info or bar_only:
        # number of dots on thermometer scale
        avail_dots = bar_width-2
        shaded_dots = int(math.ceil(float(blocks) / total_blocks * avail_dots))
        bar = "[%s%s]" % ("."*shaded_dots, " "*(avail_dots-shaded_dots))

    size_info = "%s / %s" % (min(blocks * block_size, total_size), total_size)
    # padding with spaces
    size_info = " "*(size_field_width-len(size_info)) + size_info
    if full_info:
        sys.stdout.write("\r%s %s" % (bar, size_info))
    elif size_only:
        sys.stdout.write("\r%s" % size_info)
    elif bar_only:
        sys.stdout.write("\r%s" % bar)
    else:
        # no space to draw even a lil' bar
        # print blocks, block_size, total_size
        return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("No download URL specified")

    url = sys.argv[1]

    filename = filename_from_url(url) or "."
    # get filename for temp file in current directory
    (tf, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename+".", dir=".")
    os.fdopen(tf).close()
    os.unlink(tmpfile)

    (tmpfile, headers) = urllib.urlretrieve(url, tmpfile, progress_callback)
    shutil.move(tmpfile, filename)

    print
    print headers
    print "Saved under %s" % os.path.basename(filename)

"""
features that require more tuits for urlretrieve API
http://www.python.org/doc/2.6/library/urllib.html#urllib.urlretrieve

[x] autodetect filename from URL
[ ] autodetect filename from headers - Content-Disposition
    http://greenbytes.de/tech/tc2231/
[ ] catch KeyboardInterrupt
[ ] optionally preserve incomplete file
[x] create temp file in current directory
[ ] rename temp file automatically if exists
[ ] resume download (broken connection)
[ ] resume download (incomplete file)
[x] show progress indicator
    http://mail.python.org/pipermail/tutor/2005-May/038797.html
[ ] do not overwrite downloaded file
[ ] optionally rename downloaded file automatically if exists
[ ] optionally specify path for downloaded file

[ ] options plan
"""
