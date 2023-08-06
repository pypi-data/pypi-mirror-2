
.. rubric:: A Domain Specific Language for Timeseries Analysis.

--

:Documentation: http://packages.python.org/dynts/
:Dowloads: http://pypi.python.org/pypi/dynts/
:Source: http://github.com/quantmind/dynts
:Keywords: timeserie, quantitative, finance, statistics, web

--

Timeseries analysis and a timeseries domain specific language written in Python.


Timeserie Object
========================

To create a timeseries object directly::

	>>> from dynts import timeseries
	>>> ts = timeseries('test')
	>>> ts.type
	'zoo'
	>>> ts.name
	'test'
	>>> ts
	TimeSeries:zoo:test
	>>> str(ts)
	'test'


DSL
=======
At the core of the library there is a Domain-Specific-Language (DSL_) dedicated
to timeserie analysis and manipulation. DynTS makes timeserie manipulation easy and fun.
This is a simple multiplication::
	
	>>> import dynts
	>>> e = dynts.parse('2*GOOG')
	>>> e
	2.0 * goog
	>>> len(e)
	2
	>>> list(e)
	[2.0, goog]
	>>> ts = dynts.evaluate(e).unwind()
	>>> ts
	TimeSeries:zoo:2.0 * goog
	>>> len(ts)
	251


Requirements
=====================
There are several requirements that must be met:

* python_ 2.5 or later. Note that Python 3 series are not supported yet.
* numpy_ for arrays and matrices.
* ply_ the building block of the DSL_.
* rpy2_ if an R_ TimeSeries back-end is used (default).
* ccy_ for date and currency manipulation.

Depending on the back-end used, additional dependencies need to be met.
For example, there are back-ends depending on the following R packages:

* zoo_ and PerformanceAnlytics_ for the ``zoo`` back-end (currently the default one)
* timeSeries_ for the ``rmetrics`` back-end 

Installing rpy2_ on Linux is straightforward, on windows it requires the
`python for windows`__ extension library.

Optional Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* xlwt_ to create spreadsheet from timeseries.
* simplejson_ if python_ version is less then 2.6
* matplotlib_ for plotting.
* djpcms_ for the ``web.views`` module.

__ http://sourceforge.net/projects/pywin32/files/

Running Tests
=================
Form the package directory::
	
	python runtests.py
	
or, once installed::

	from dynts import runtests
	runtests()
	
If you are behind a proxy, some tests will fail unless you write a little script
which looks like this::

	from dynts.conf import settings
	from dynts import runtests
	settings.proxies['http'] = 'http://your.proxy.com:80'

	if __name__ == '__main__':
	    runtests()
	    
	    
Community
=================
Trying to use an IRC channel **#dynts** on ``irc.freenode.net``
(you can use the webchat at http://webchat.freenode.net/).

If you find a bug or would like to request a feature, please `submit an issue`__.

__ http://github.com/quantmind/dynts/issues
    
.. _numpy: http://numpy.scipy.org/
.. _ply: http://www.dabeaz.com/ply/
.. _rpy2: http://rpy.sourceforge.net/rpy2.html
.. _DSL: http://en.wikipedia.org/wiki/Domain-specific_language
.. _R: http://www.r-project.org/
.. _ccy: http://code.google.com/p/ccy/
.. _zoo: http://cran.r-project.org/web/packages/zoo/index.html
.. _PerformanceAnlytics: http://cran.r-project.org/web/packages/PerformanceAnalytics/index.html
.. _timeSeries: http://cran.r-project.org/web/packages/timeSeries/index.html
.. _Python: http://www.python.org/
.. _xlwt: http://pypi.python.org/pypi/xlwt
.. _simplejson: http://pypi.python.org/pypi/simplejson/
.. _matplotlib: http://matplotlib.sourceforge.net/
.. _djpcms: http://djpcms.com