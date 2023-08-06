=============================
Replacers - fake data sources
=============================

A 'replacer' is a source of faked data. The replacers in this module can be
referred to using a string that is simply the name of the function. Custom
replacers can be used by defining them as callables.

When run by the anonymizer, the callable will be passed the Anonymizer object,
the object being altered, the field being altered, and the current value of the
field. It must return random data of the appropriate type. You can use ``lambda
*args: my_constant_value`` to return a constant.

All of the replacers defined in this module use a
:class:`anonymizer.base.DjangoFaker` instance to generate fake data, and this
object may be of use to you in writing your own replacers.


.. automodule:: anonymizer.replacers
   :members:
