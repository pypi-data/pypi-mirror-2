import re
import StringIO

import IPython.genutils

class EventLogger(object):
    
    def __init__(self, capacity=100000):
        self._capacity = capacity
        self._records = []
        
    def push_event(self, evt):
        attr_name = evt.attr_name
        dev, sep, attr = attr_name.rpartition('/')
        if dev.startswith("tango://"):
            dev = dev[8:]
        if dev.count(":"):
            # if it has tango host
            host, sep, dev = dev.partition('/')
        else:
            host = "-----"
        evt.host = host
        evt.dev_name = dev
        evt.s_attr_name = attr
        self._records.append(evt)
        over = len(self._records) - self._capacity
        if over > 0:
            self._records = self._records[over:]
    
    def model(self):
        return self
    
    def getEvents(self):
        return self._records
    
    def show(self, dexpr=None, aexpr=None):
        if dexpr is not None:
            dexpr = re.compile(dexpr, re.IGNORECASE)
        if aexpr is not None:
            aexpr = re.compile(aexpr, re.IGNORECASE)
            
        s = StringIO.StringIO()
        cols = 4, 30, 18, 20, 12, 16
        l = "%{0}s %{1}s %{2}s %{3}s %{4}s %{5}s".format(*cols)
        print >>s, l % ('ID', 'Device', 'Attribute', 'Value', 'Quality', 'Time')
        print >>s, l % (cols[0]*"-", cols[1]*"-", cols[2]*"-", cols[3]*"-", cols[4]*"-", cols[5]*"-")
        for i,r in enumerate(self._records):
            if dexpr is not None and not dexpr.match(r.dev_name): continue
            if aexpr is not None and not aexpr.match(r.s_attr_name): continue
            if r.err:
                v = r.errors[0].reason
                q = 'ERROR'
                ts = r.reception_date.strftime("%H:%M:%S.%f")
            else:
                v = str(r.attr_value.value)
                q = str(r.attr_value.quality)
                ts = r.attr_value.time.strftime("%H:%M:%S.%f")
            print >>s, l % (i, r.dev_name, r.s_attr_name, v, q, ts)
        s.seek(0)
        IPython.genutils.page(s.read())