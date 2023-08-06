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

Licensing
*********
Copyright (c) 2011 Votizen Incorporated

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.