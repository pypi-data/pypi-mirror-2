.. _usage:

Howto use the library
=====================

Its easy to get started with the :doc:`mockups management command
<mockups>` but its quite limited if you want to have more control of how
your test data should be created. This chapter describes how you use the
library in your python environment like the shell, a custom script or in
unittests.

Creating model instances
------------------------

The :mod:`mockups` module contains a few shortcuts to make the creation of
test data as fast as possible.

.. _shortcuts:

.. autofunction:: mockups.create

.. autofunction:: mockups.create_one

.. _ModelMockup:

Using the ModelMockup class
----------------------

.. autoclass:: mockups.base.ModelMockup
   :members: __init__, add_field_generator, add_constraint, check_constrains,
       create, create_one

Subclassing :class:`ModelMockup`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following methods may be overwritten by subclasses:

.. automethod:: mockups.base.ModelMockup.prepare_class

.. automethod:: mockups.base.ModelMockup.post_process_instance

.. automethod:: mockups.base.ModelMockup.get_generator
