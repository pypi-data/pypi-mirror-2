===============
Django crypto
===============

Django-crypto is small package that simplifies 2-way encryption for Django developers. This is very useful when you want to send data to Users, but don't want them to be able to edit it, such as password reset tokens.

Install
=======

Source code is location at https://github.com/votizen/django-crypto.

Simply run::

python setup.py install

In your Django app settings add::

INSTALLED_APPS = (...,
	'django_crypto',
)

CRYPTO_SECRET = 'REPLACE WITH A RANDOM STRING'


Usage
=====

from django_crypto import DecodeAES, EncodeAES

str = 'test string'

# encode a string
encoded_str = EncodeAES(str)

# decode a string
original_str = DecodeAES(encoded_str)


History
=======

	* Version 0.1.0 released 8/14/2011, includes encode and decode strings, 

TODO
====

    * Nothing yet