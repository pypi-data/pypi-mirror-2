Welcome to django-mockups's documentation!
==============================================
This app aims to provide a simple way of loading masses of randomly generated
test data into your development database. You can use a :ref:`management
command <mockups>` to load test data through command line.

Usually you add test data through the admin to see how your site looks with non
static pages. You export data by using ``dumpdata`` to send it to your
colleagues or to preserve it before you make a ``manage.py reset app`` and so
on. Your site gets more and more complex and adding test data gets more and
more annoying.

This is the usecase where mockups should help you to save time that can
actually be spent on hacking.

.. _contents:

Contents
========

.. toctree::
    :maxdepth: 2

    installation
    mockups
    usage
    registry
    contribute
