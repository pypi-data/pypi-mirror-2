Changelog
=========

0.4.4
-----
* Rename and remake ChoicesGenerator -> ChoiceGenerator + ChoiceFieldGenerator

0.4.3
-----
* Make generators take empty_value keyword argument

0.4.2
-----
* Make ModelMockup take a factory instance as keyword argument for more
  flexibility

0.4.1
-----
* Just a rename of Mockup to ModelMockup

0.4.0
-----
* Major rewrite to use Factory

0.2.6
-----
* Changing syntax to match Django Models & Forms

* Renaming to django-mockups


0.2.5
-----

* Fixing issue with ``--generate-fk`` option in management command. Thanks
  Mikko Hellsing for the `report and fix`_.

.. _report and fix: http://github.com/gregmuellegger/django-autofixture/issues/issue/1/

0.2.4
-----

* Using ``Autofixture.Values`` for defining initial values in ``Autofixture``
  subclasses.

* Making autodiscover more robust. Don't break if some module can't be
  imported or throws any other exception.

0.2.3
-----

* Fixing bug when a ``CharField`` with ``max_length`` smaller than 15 is used.

* ``Mockup.field_generators`` accepts callables as values.
