ccy
===========

Python module for currencies. The module compiles a dictionary of currency objects containing
information useful in financial analysis.

Not all currencies in the world are supported yet.
You are welcome to join and add more.

Installation
=================
Using `easy_install`::

	easy_install ccy
	
Using `pip`::

	pip install ccy
	
From source::

	python setup.py install
	
	
Runnung tests
==================
From within the package directory::

	python runtests.py
	
or, once installed::

    >> from ccy import runtests
    >> runtests()
    
    
Trading Centres
====================
Support trading centres date calculation::

    >>> from ccy.tradingcentres import nextbizday, datetime
    >>> d1 = datetime.date(2010,4,2)
    >>> nextbizday(d1,2)
    datetime.date(2010, 4, 6)
	