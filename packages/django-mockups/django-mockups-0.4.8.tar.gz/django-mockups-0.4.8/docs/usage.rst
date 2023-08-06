.. _usage:

Howto use the library
=====================
Its easy to get started with the :ref:`mockups <mockups>` management command
but its quite limited if you want to have more control of how your test data
should be created. This chapter describes how you use the library in your
python environment like the shell, a custom script or in unittests.


Creating model instances
------------------------
The :mod:`mockups` module contains a few shortcuts to make the creation of
test data as fast as possible.

.. _shortcuts:

.. autofunction:: mockups.create

.. autofunction:: mockups.create_one


.. _Mockup:

Using the Mockup class
---------------------------
.. autoclass:: mockups.base.Mockup
   :members: __init__, update_fieldname_generator, add_constraint, check_constrains,
       create, create_one


Subclassing :class:`Mockup`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The following methods may be overwritten by subclasses:

.. automethod:: mockups.base.Mockup.prepare_class

.. automethod:: mockups.base.Mockup.post_process_instance

.. automethod:: mockups.base.Mockup.get_generator
