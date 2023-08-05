`buildout.locallib` use egg-packages installed on site-packages folder.

`zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ check
package installation by zc.buildout.easy_install.Installer that
exclude /path/to/site-packages folder path for checking.

When 'site-packages' folder include some easy-installed packages,
We want to re-use these packages in some cases.


Using sample
------------

site-packages include some eggs::

   $ ls /path/to/site-packages
   easy-install.pth
   pip-0.6.3-py2.6.egg/
   pastedeploy-1.3.3-py2.6.egg/
   pastescript-1.7.3-py2.6.egg/
   paste-1.7.4-py2.6.egg/
   setuptools-0.6c11-py2.6.egg
   setuptools.pth


write buildout.cfg::

   [buildout]
   parts = foo

   [foo]
   recipe = zc.recipe.egg
   eggs =
       PasteScript


run bootstrap and buildout::

   $ python bootstrap.py
   $ bin/buildout -U
   ...

list eggs dir::

   $ ls eggs
   zc.recipe.egg-1.2.3b2-py2.6.egg
   pastescript-1.7.3-py2.6.egg
   pastedeploy-1.3.3-py2.6.egg
   paste-1.7.4-py2.6.egg

(clean-up)::

   $ rm -R eggs

Now update buildout.cfg to use `buildout.locallib` extension::

   [buildout]
   parts = foo
   extensions = buildout.locallib
   ...

And run buildout again::

   $ bin/buildout -U
   ...

Check your eggs folder again::

   $ ls eggs
   buildout.locallib-0.0.1-py2.6.egg
   zc.recipe.egg-1.2.3b2-py2.6.egg

If package exists at site-packages folder, now using installed version
packages.


Requirements
------------

* Python 2.4 or later


Dependencies
------------

* `setuptools <http://pypi.python.org/pypi/setuptools>`_ or
  `distribute <http://pypi.python.org/pypi/distribute>`_

* `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_


Features
--------

* Extends zc.buildout functionality to search installed packages.


Setup
-----

Write buildout.cfg with `extensions = buildout.locallib`::

   [buildout]
   parts = foo
   extensions = buildout.locallib
   ...


ToDo
-----
* Add support script for create dummy `egg-info` folders.
* Write tests.


History
-------

0.1.0 (2010-6-27)
~~~~~~~~~~~~~~~~~~
* first release

