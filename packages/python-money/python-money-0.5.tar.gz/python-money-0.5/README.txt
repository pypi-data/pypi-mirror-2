Python-Money
============

Introduction
------------

python-money provides carefully designed basic Python primitives for working with money and currencies.

The primary objectives of this module is to aid in the development of financial applications by increasing testability and reusability, reducing code duplication and reducing the risk of defects occurring in the code.

The module defines two basic Python classes -- a Currency class and a Money class. It also pre-defines all the world's currencies, according to the ISO 4217 standard. The classes define some basic operations for working with money, overriding Python's addition, substraction, multiplication, etc. in order to account for working with money in different currencies. They also define currency-aware comparison operators. To avoid floating point precision errors in monetary calculations, the module uses Python's Decimal type exclusively.

The design of the module is based on the Money enterprise design pattern, as described in Martin Fowler's "Patterns of Enterprise Application Architecture".

This project also contains Django helper classes for easy integration with python-money.

Installation
------------

    python setup.py install

Project Site
------------
http://code.google.com/p/python-money/

*This project is sponsored by* `A115 Ltd <http://www.a115.bg/>`_.
