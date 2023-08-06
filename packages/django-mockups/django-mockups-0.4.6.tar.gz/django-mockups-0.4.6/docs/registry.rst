The mockup registry
===================
.. _registry:

Since :class:`Mockup` is designed to fit for almost all models, its very
generic and doesn't know anything about the actual logic and meanings of
relations or the purpose of your model fields.

So there is a registry to register custom :class:`Mockup` subclasses with
specific models. These subclasses are then used by default if you generated
test data either with the :ref:`mockups <mockups>` management
command or with one of the :ref:`shortcuts <shortcuts>` in :mod:`mockups`.

.. autofunction:: mockups.register

.. autofunction:: mockups.unregister


Included Mockup subclasses
-------------------------------
There are some :class:`Mockup` subclasses that are shipped by default
with ``django-mockups``. These are listed below.

.. _UserMockup:
.. autoclass:: mockups.contrib.auth.UserMockup
   :members: __init__
