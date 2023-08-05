# coding=utf-8
import codecs

# can be found in lujo.utils too
def to_unicode(s, cp="utf-8"):
    assert cp in ("utf8", "utf-8", "cp1250"), cp
    if isinstance(s, str):
        s = unicode(s, cp)
    assert isinstance(s, unicode),s
    return s

def from_unicode(s, cp="utf-8"):
    assert cp in ("utf8", "utf-8", "cp1250"), cp
    assert isinstance(s, unicode),s
    return codecs.encode(s, cp)

def iter_mine(*args):
    """
    for val in iter_mine():
        print val
    for val in iter_mine(2):
        print val
    for val in iter_mine(2,3):
        print val
    for val in iter_mine(2,3,2):
        print val
    #for val in iter_mine(2,3,2,1):
    #    print val
    """
    if not args:
        yield ()
        return
    # print "iter:", args
    for arg in args:
        assert isinstance(arg, int)
    if len(args)==1:
        for arg0 in range(args[0]):
            yield (arg0,)
    elif len(args)==2:
        for arg0 in range(args[0]):
            for arg1 in range(args[1]):
                yield (arg0, arg1)
    elif len(args)==3:
        for arg0 in range(args[0]):
            for arg1 in range(args[1]):
                for arg2 in range(args[2]):
                    yield (arg0, arg1, arg2)
    else:
        raise Exception("not implemented %d len" % (len(args),))

def get_exc_str():
    import traceback
    exc_info=sys.exc_info()
    if not exc_info[0]:
        return "No py exception"
    out="%s/%s/%s" % (str(exc_info[0]), str(traceback.extract_tb(exc_info[2])), str(exc_info[1]))
    #if bClear: sys.exc_clear()
    return out

# useful template
# doctest: +NORMALIZE_WHITESPACE
def test():
    print "%s: running doctests" % __name__
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()
