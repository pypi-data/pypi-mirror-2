====================================
DjangoFaker - Django-aware fake data
====================================

.. class:: anonymizer.base.DjangoFaker

   This class is used by the :mod:`anonymizer.replacers` module to generate fake
   data. It encapsulates some knowledge about Django models and fields to
   attempt to generate data that fits the constraints of the model.

   .. method:: get_allowed_value(self, source, field)

      This method is the part that encapsulates knowledge about Django models
      and fields, and uses it to return appropriate data.

      ``source`` is a callable that takes no arguments and returns a piece of
      fake data. In some cases (such as for unique constraints), it may be
      necessary for this callable to called more than once, to try to get data
      that doesn't violate constraints.

      ``field`` is the Django model field for which data must be generated. If
      ``None``, the source callable will be used without further checking.

       So far, this method understands and attempts to respect:

       * The ``max_length`` attribute of fields.

       * The ``unique`` constraint.


   The remaining public methods all generate different types of fake data, using
   ``get_allowed_value`` to apply constraints. Many methods use an underlying
   ``faker.Faker`` instance. These include the following, which have some useful
   properties.

   .. method:: name(self)

      Generates a full name, using the '<first name> <last name>' pattern.

   .. method:: first_name(self)

      Returns a randomly selected first name

   .. method:: last_name(self)

      Returns a randomly selected last name

   .. method:: email(self)

      Returns a randomly generated email address, using the pattern
      '<initial><last name>@<free email provider>'

   .. method:: username(self)

      Returns a randomly generated user name, using the pattern
      '<initial><lastname>'.

   These name-related methods have the property that the same underlying first
   name and last name will be used until you repeat any of the methods. This
   means that if you use these methods to generate a set of data for a user
   model, the name/username/email address for a single object will correspond to
   each other.

   For models with unique constraints on one of these fields, there is the
   complication that django-anonymizer will avoid setting unique fields to
   already present or already generated values. Sometimes this means that a fake
   data source must be used more than once to get a unique value, and this can
   upset the state of the cycle. To avoid this, put fields with a unique
   constraint at the start of the :attr:`~anonymizer.base.Anonymizer.attributes`
   list.
