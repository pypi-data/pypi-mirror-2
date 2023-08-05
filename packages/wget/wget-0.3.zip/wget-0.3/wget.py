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


version = "0.3"


def filename_from_url(url):
    """:return: detected filename or None"""
    fname = os.path.basename(urlparse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("No download URL specified")

    url = sys.argv[1]

    filename = filename_from_url(url) or "."
    # get filename for temp file in current directory
    (tf, tmpfile) = tempfile.mkstemp(".tmp", prefix=filename+".", dir=".")
    os.fdopen(tf).close()
    os.unlink(tmpfile)

    (tmpfile, headers) = urllib.urlretrieve(url, tmpfile)
    shutil.move(tmpfile, filename)

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
[ ] show progress indicator
    http://mail.python.org/pipermail/tutor/2005-May/038797.html
[ ] do not overwrite downloaded file
[ ] optionally rename downloaded file automatically if exists
[ ] optionally specify path for downloaded file

[ ] options plan
"""
