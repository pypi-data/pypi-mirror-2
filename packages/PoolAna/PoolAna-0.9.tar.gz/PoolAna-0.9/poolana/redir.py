from ctypes import PyDLL, CDLL, c_void_p, c_char_p, py_object
from os import dup, dup2, fsync
from sys import stdout
from contextlib import contextmanager

_pyapi = PyDLL(None)
_pyapi.PyFile_AsFile.restype = c_void_p
_pyapi.PyFile_AsFile.argtypes = [py_object]

_this_exe = CDLL(None)
_this_exe.freopen.restype = c_void_p
_this_exe.freopen.argtypes = [c_char_p, c_char_p, c_void_p]

def _freopen(filename, mode, pyfile):
    return _this_exe.freopen(filename, mode, _pyapi.PyFile_AsFile(pyfile))

@contextmanager
def redir(filename, stream=stdout):
    """Redirect all output (by file descriptor, so 'all' includes C/C++ extension
    modules) on the given stream to the given filename."""
    try:
        saved_stream_fd = dup(stream.fileno())
        _freopen(filename, "w", stream)
        yield
    finally:
        stream.flush()
        fsync(stream.fileno())
        dup2(saved_stream_fd, stream.fileno())

#if __name__=='__main__':
#    print "stuff"
#    with redir('foo.txt'):
#        print "logged"
#    print "not logged"
