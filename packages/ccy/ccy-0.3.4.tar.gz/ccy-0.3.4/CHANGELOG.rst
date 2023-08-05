ccy 0.3.4  - 2010 April 25
=============================
 * Added trading centres for calculation of trading holidays (requires python-dateutil)
 * This feature is still very much alpha.

ccy 0.3.3  - 2010 March 31
=============================
 * Added `ccy.basket.media` to `MANIFEST.in`

ccy 0.3.2  - 2010 March 30
=============================
 * Added `ccy.basket` module, a django application for managing basket of currencies.

ccy 0.3
==============
 * Added as_cross to ccy class to display the currency as a cross FX string
 * Added 2 shortcuts to display crosses: cross(eur) -> EURUSD, and crossover(eur) -> EUR/USD
 
ccy 0.2
==============
 * THIS VERSION IS NOT COMPATIBLE WITH PREVIOUS ONE
 * Rearranged the modules so that data-structures and data are separated.
 * Added symbol property to ccy
 * bug fixes and refactoring for python 3.1 compatibility
 * Added another 2 tests
 
ccy 0.1.2
============
first official release
 