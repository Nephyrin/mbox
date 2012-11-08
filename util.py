#!/usr/bin/env python2

import os
import stat
import shutil
import string

from os.path import exists
from os.path import join
from os.path import normpath

from collections import defaultdict

def safecopy(src, dst):
    assert file_exists(src) and not file_exists(dst)
    # check if use slice syscall
    shutil.copyfile(src, dst)

def safestat(pn):
    try:
        return os.stat(pn)
    except OSError:
        return None

def dir_exists(pn):
    s = safestat(pn)
    return s and stat.S_ISDIR(s.st_mode)

def file_exists(pn):
    s = safestat(pn)
    return s and stat.S_ISREG(s.st_mode)

def mkdir(pn):
    try:
        return os.mkdir(pn)
    except OSError:
        pass

def chjoin(root, *paths):
    pn = [p.lstrip("/") for p in paths]
    np = normpath(join(root, *pn))

    # escaped by multiple ..
    if not np.startswith(root):
        return root
    return np

def itercrumb(path, strip=False):
    assert path.startswith("/")
    pn = path.rstrip("/")
    pn = normpath(pn)

    head = "/"
    for crumb in pn[1:].split("/"):
        head += crumb + "/"
        if strip:
            yield head[1:]
        else:
            yield head

def to_printable(c):
    return c if c in string.printable else "."

def hexdump(binstr):
    hexstr = map(lambda c : "%02X" % ord(c), binstr)
    hexstr.extend(["  "] * 0x10)

    line = []
    for offset in range(0, len(hexstr)/0x10):
        s = offset * 0x10
        e = s + 0x10
        line.append("%08X: %s %s\n" \
          % (s, " ".join(hexstr[s:e]),
             "".join(map(to_printable, binstr[s:e]))))

    return "".join(line)

def which(prog):
    path = os.environ.get("PATH", "")
    for d in path.split(":") + ["."]:
        pn = join(d, prog)
        if exists(pn):
            return pn
    raise Exception("Can't find %s" % prog)
