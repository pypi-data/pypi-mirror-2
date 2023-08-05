
try:
    import IPython
except:
    IPython = None

def get_ipython_version():
    """Returns the current IPython version"""
    if IPython is None:return None
    v = None
    try:
        try:
            v = IPython.Release.version
        except Exception, e1:
            try:
                v = IPython.release.version
            except Exception, e2:
                pass
    except Exception, e3:
        pass
    return v

def default_init_ipython(ip, store=True, pytango=True, colors=True, console=True, magic=True):
    print "Unsupported IPython version (%s) for spock profile" % get_ipython_version()
    print "Supported IPython versions are: 0.10"
    print "Starting normal IPython console..."

def __define_init():
    _ipv_str = get_ipython_version()

    if _ipv_str is None:
        _ipv = 0,0
    else:
        _ipv = tuple(map(int,_ipv_str.split(".")[:3]))

    ret = default_init_ipython
    if _ipv >= (0,10) and _ipv <= (0,11):
        import ipython_00_10
        ret = ipython_00_10.init_ipython
    return ret

init_ipython = __define_init()
#init_ipython(IPython.ipapi.get())
