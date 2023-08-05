Django Authentication Module
============================

.. module:: openid2rp

A small Django authentication backend for OpenID, based on the openid2rp package.
It is automatically installed together with openid2rp. 

In order to get the Django database magic right, you need to add 'openid2rp.django' to your 
INSTALLED_APPS list in setup.py. You also need to add 'openid2rp.django.auth.Backend' to the
list of authentication backends. Example::

  INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'openid2rp.django',
	'<yourapp>.front'
  )

  AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'openid2rp.django.auth.Backend'
  )

The database is extended with one table for the	 OpenID identifier storage. 
Therefore, make sure that you call "python manage.py syncdb" ones 
after installing this package.

In contrast to most other Django OpenID authentication packages, this one
does not try to cover any view aspects. It also keeps the nature of openid2rp
by assuming that you know how OpenID works. 

Since the Django authentication framework is not prepared for a multi-step auth scenario with several 
inputs and outputs, you need to call a preparation function ("preAuthenticate") from the module
before you can use the Django authenticate() method. make sure that you use the correct keyword
arguments in the authenticate() call.

Session storage is based on a module-scope variable. I was to lazy to decode the openid2rp session dict
for the database storing and lifetime checking. There is also no Nonce checking so far.

The explicit modeling of each exceptional case hopefully allows you to realize an according 
reaction in your view rendering. 
