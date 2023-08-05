from __future__ import with_statement

import ctypes, os.path, sys, os

if (hasattr(sys, 'maxsize') and sys.maxsize != 2**31-1
    or hasattr(sys, 'maxint') and sys.maxint != 2**31-1):
    print('The Poker Sleuth scriptable equity calculator is a 32-bit DLL and can only be used from a 32-bit version of Python.  You will need to install the 32-bit version of Python to use this module.')
    sys.exit(1)

if sys.version_info[0] >= 3:
    getenv = os.getenv
    unicode = str
    import http.client as httplib
    raw_input = input
    no_bytes = bytes()
else:
    import httplib
    def getenv(name):
        name = unicode(name)
        n = ctypes.windll.kernel32.GetEnvironmentVariableW(name, None, 0)
        if n == 0:
            return None
        buf = ctypes.create_unicode_buffer(unicode('\0')*n)
        ctypes.windll.kernel32.GetEnvironmentVariableW(name, buf, n)
        return buf.value
    no_bytes = str()

path = os.path.join(getenv('PROGRAMFILES'),
                    unicode('PokerSleuth\\montecarlo.dll'))
if not os.path.exists(path):
    answer = raw_input("Poker Sleuth could not be found.  Would you like to download it? [Y/n] ")
    if answer.strip() and answer[0].lower() != 'y':
        sys.exit(1)
    conn = httplib.HTTPConnection('pokersleuth.com')
    conn.request('GET', '/dist/PokerSleuthInstaller.exe')
    r = conn.getresponse()
    length = r.getheader('content-length')
    if r.status != 200:
        print("Download error")
        sys.exit(1)
    parts = []
    data = True
    completion = 0
    bar = 0
    while data:
        data = r.read(16384)
        parts.append(data)
        completion += len(data)
        while completion / float(length) > bar / float(80):
            sys.stdout.write('=')
            sys.stdout.flush()
            bar += 1
    sys.stdout.write('\n')
    data = no_bytes.join(parts)
    with open('PokerSleuthInstaller.exe', 'wb') as f:
        f.write(data)
    os.system('PokerSleuthInstaller.exe')
    sys.exit(1)

montecarlo = ctypes.CDLL(path)

class cParseError(ctypes.Structure):
    _fields_ = [('player', ctypes.c_int),
                ('first_column', ctypes.c_int),
                ('last_column', ctypes.c_int),
                ('msg', ctypes.c_char*256)]

montecarlo.compute_equity.restype = ctypes.c_int
montecarlo.compute_equity.argtypes = [ctypes.c_int,
                            ctypes.POINTER(ctypes.c_char_p),
                            ctypes.c_char_p,
                            ctypes.POINTER(ctypes.c_double),
                            ctypes.POINTER(cParseError)]

class ParseError(Exception):
    pass

def compute_equity(board, ranges):
    n = len(ranges)
    cparray = ctypes.c_char_p*n
    pe = cParseError()
    out = (ctypes.c_double*n)()
    ranges = (ctypes.c_char_p*n)(*ranges)

    err = montecarlo.compute_equity(len(ranges), ranges, board, out,
                                    ctypes.byref(pe))
    if err:
        raise ParseError('%d:%d:%d: %s' % (pe.player,
                                           pe.first_column, pe.last_column,
                                           pe.msg))
    return list(out)

__all__ = ['compute_equity', 'ParseError']

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: equitycalc board holes ...\n")
        sys.exit(1)
    board = sys.argv[1]
    ranges = sys.argv[2:]
    print(compute_equity(board, ranges))
