import time,datetime
import types, operator
from _PyTango import TimeVal

def __TimeVal__init__(self, a=None, b=None, c=None):
    TimeVal.__init_original__(self)
    if a is None: 
        return

    if isinstance(a, datetime.datetime):
        assert(b is None and c is None)
        a = time.mktime(a.timetuple()) + a.microsecond*1E-6

    elif operator.isNumberType(a):
        if b is None:
            self.tv_sec = int(a)
            usec = (a - self.tv_sec) * 1E6
            self.tv_usec = int(usec)
            self.tv_nsec = int((usec - self.tv_usec) * 1E3)
        else:
            self.tv_sec, self.tv_usec, self.tv_nsec = a, b, c


def __init_TimeVal():
    TimeVal.__init_original__ = TimeVal.__init__
    TimeVal.__init__ = __TimeVal__init__
    TimeVal.totime = lambda self : self.tv_sec + 1E-6*self.tv_usec + 1E-9*self.tv_nsec
    TimeVal.todatetime = lambda self : datetime.datetime.fromtimestamp(self.totime())
    TimeVal.fromtimestamp = staticmethod(lambda ts : TimeVal(ts))
    TimeVal.fromdatetime = staticmethod(lambda dt : TimeVal(dt))
    TimeVal.now = staticmethod(lambda : TimeVal(time.time()))
    TimeVal.strftime = lambda self : self.todatetime().strftime(f)
    TimeVal.isoformat = lambda self : self.todatetime().isoformat(f)
    TimeVal.__str__ = lambda self : str(self.todatetime())
    
def init_TimeVal():
    __init_TimeVal()