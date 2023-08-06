from django import http
from djpcms.views import appview

from ccy import date2yyyymmdd, dateFromString


def date2yyyymmdd(dte):
    return dte.day + 100*(dte.month + 100*dte.year)

class TimeSeriesView(appview.AppView):
    '''```djpcms``` application view which can be used to obtain timeseries.
The only view available is an Ajax Get response.'''
    _methods      = ('get',)
    
    def get_response(self, djp):
        request = djp.request
        if not request.is_ajax():
            raise http.Http404
        sdata = self.econometric_data(dict(request.GET.items()))
        return http.HttpResponse(sdata, mimetype='application/javascript')
    
    def get_object(self, code):
        '''Check if the code is an instance of a model.'''
        codes = code.split(':')
        if len(codes) == 2 and codes[0] == str(self.model._meta):
            try:
                return self.model.objects.get(id = int(codes[1]))
            except:
                return None
                
    def econometric_data(self, data):
        cts    = data.get('command',None)
        start  = data.get('start',None)
        end    = data.get('end',None)
        period = data.get('period',None)
        object = self.get_object(cts)
        if object:
            cts = self.codeobject(object)
        if start:
            start = dateFromString(str(start))
        if end:
            end = dateFromString(str(end))
        try:
            return self.getdata(cts,start,end)
        except IOError, e:
            return ''
    
    def codeobject(self, object):
        return str(object)
    
    def getdata(self,cts,start,end):
        '''Pure virtual function which needs to be implemented by implementations.
It retrieve the actual timeseries data.'''
        raise NotImplementedError
    
    