from setuptools import setup, find_packages
import sys, os
 
README = r"""
repoze.what.plugins.ip
======================

It is a repoze.what_ plugin that provides an ip_from predicate.

Installation
------------

easy_install_::

    $ <env>/bin/easy_install repoze.what.plugins.ip

pip_::

    $ <env>/bin/pip install repoze.what.plugins.ip

Source
------

The source code can be found at code.google.com_.

Usage
-----

``ip_from([allowed=None], [proxies=None])`` checks whether REMOTE_ADDR in the
environment points to an allowed IP address. If HTTP_X_FORWARDED_FOR is set
in the environment (meaning proxy access) then REMOTE_ADDR is treated as a proxy
address and HTTP_X_FORWARDED_FOR as an originating IP address.

``allowed`` optional, default - ``None``
    A list of IPs to allow access. Can be a string which is then interpreted as
    a single IP address

``proxies`` optional, default - ``None``
    If a list or tuple provided then treated as a list of authorized proxy IP
    addresses.

    If a string or unicode provided then treated as a single IP address.

    Any other value - ``bool(proxies) == True`` means that all proxies are
    accepted

You can filter the incoming IP address::

    >>> from repoze.what.plugins.ip import ip_from
    >>> p = ip_from(allowed=['192.168.1.1'])
    >>> env = {'REMOTE_ADDR': '192.168.1.1'}
    >>> p.is_met(env)
    True
    >>> env = {'REMOTE_ADDR': '192.168.1.10'}
    >>> p.is_met(env)
    False

By default proxy access is disabled. You can enable it with ``proxies=True``::

    >>> p = ip_from(allowed=['192.168.0.0/24'], proxies=True)
    >>> env = {
    ...     'REMOTE_ADDR': '192.168.1.1',           # proxy
    ...     'HTTP_X_FORWARDED_FOR': '192.168.1.5'   # origin
    ... }
    >>> p.is_met(env)
    True

And you can also explicitly specify proxies to allow::

    >>> p = ip_from(allowed='192.168.1.5', proxies=['192.168.0.0/24'])
    >>> env = {
    ...     'REMOTE_ADDR': '192.168.1.1',           # proxy
    ...     'HTTP_X_FORWARDED_FOR': '192.168.1.5'   # origin
    ... }
    >>> p.is_met(env)
    True

.. _repoze.what: http://what.repoze.org/docs/1.0/ 
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall 
.. _pip: http://pip.openplans.org/ 
.. _code.google.com: http://code.google.com/p/repoze-what-plugins-ip/ 
"""

version = "0.2"

setup(name='repoze.what.plugins.ip',
      version=version,
      description='ip based restrictions for repoze.what.',
      long_description=README,
      classifiers=[],
      keywords='''wsgi repoze what paste paster google ip ipaddr proxy
      remote_addr x_forwarded_for http_x_forwarded_for''',
      author='Vince Spicer',
      author_email='vinces1979@gmail.com',
      url='http://code.google.com/p/repoze-what-plugins-ip',
      license='Apache 2.0',
      packages=find_packages(exclude=['tests']),
      #package_data=package_data,      
      include_package_data=True,
      zip_safe=False,
      tests_require=['nose'],
      test_suite="nose.collector",
      install_requires=['repoze.what'],
      namespace_packages=['repoze', 'repoze.what', 'repoze.what.plugins'],
      entry_points='',
      )
