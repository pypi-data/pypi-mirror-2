Installation
============

Download and install with pip or easy_install
---------------------------------------------
You can install the ``django-mockups`` like any other python package. The
prefered way is to use `pip <http://pypi.python.org/pypi/pip>`_. Please run the
following command in your terminal::

    pip install django-mockups

This will install the package in your system wide python installation.

You can fall back to the :command:`easy_install` command if :command:`pip` is
not available on your system::

    easy_install django-mockups

.. note:: In most cases you need admin previlegies to install a package into
   your system. You can get these previlegies by prefixing the commands above
   with ``sudo``.

.. _INSTALLED_APPS:


Add mockups to your django project
----------------------------------
Usually you want to add ``mockups`` to your ``INSTALLED_APPS`` in the
settings file of your django project. This will make the :ref:`mockups
<mockups>` management command available to your use.


Using the development version
-----------------------------
You can ofcourse also install and use the current development version. All you
need is to have the `git <http://git-scm.com/>`_ and `setuptools
<http://pypi.python.org/pypi/setuptools>`_ installed.

Now get the repository from `github
<http://github.net/sorl/django-mockups>`_ and run::

    git clone git://github.com/sorl/django-mockups.git

This will download the project into your local directory. :command:`cd` to the
``django-mockups`` directory and run::

    python setup.py install

Now follow the instructions under :ref:`INSTALLED_APPS` and everything will be
in place to use ``django-mockups``.
