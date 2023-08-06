from itertools import izip
from rpy2.robjects import IntVector

import dynts
from dynts.conf import settings
from dynts.backends.rbase import rts

 
def v2bool(v):
    try:
        return v[0]
    except:
        return False
    

def tozoo(ts):
    if isinstance(ts,TimeSeries):
        if ts.type == 'zoo':
            return ts
        else:
            raise NotImplementedError('Cannot convert %s to zoo timeserie' % ts)
    else:
        raise ValueError('%s is not a timeserie object' % ts)


class TimeSeries(rts):
    type = 'zoo'
    libraries = ['zoo,PerformanceAnalytics']
    
    def factory(self, date, data, raw = False):
        if not raw:
            tdate = self.dateconvert
            date = IntVector([tdate(dt) for dt in date])
        #data = FloatVector(data)
        return self.r['zoo'](data,date)
    
    def colnames(self):
        #TODO: Not working since we did not set names
        return self.r['colnames'](self._ts)
    
    def _rollapply(self, func, window = None, name = None, **kwargs):
        name = name or '%s(%s)' % (func,self.name)
        fun    = self.r[func]
        return self.rcts('rollapply', window, fun, name = name, **kwargs)
    
    def start(self):
        return self.dateinverse(self.rc('start')[0])
        
    def end(self):
        return self.dateinverse(self.rc('end')[0])
    
    def _mergesingle(self, ts, all = True):
        ts = tozoo(ts)
        name = settings.splittingnames.join(self.names() + ts.names())
        return self.rcts('merge', ts._ts, all = all, name = name)
    
    def merge(self, ts, all = True):
        if dynts.istimeseries(ts):
            return self._mergesingle(ts, all = all)
        else:
            rs = self
            for t in ts:
                rs = rs._mergesingle(t, all = all)
            return rs
    