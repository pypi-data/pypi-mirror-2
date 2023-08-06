================================
Application programmer interface
================================

Overview
========

Additionally to the command line tool ``cutplace`` all functions are available
as Python API. For a complete reference about all public classes and functions,
visit <http://cutplace.sourceforge.net/api/>.

The remainder of this chapter focuses on describing how to perform a basic
validation of a simple CSV file containing data about some customers.

Set up logging
==============

Cutplace uses Python's standard logging module. This provides a familiar and
powerful way to watch what cutplace is doing. However, it also requires to
setup the logging properly in order to gain most from it.

For a quick start, set up your application's log messages to go to the console
and show only information, warning and errors, but no debug messages:

>>> import logging
>>> logging.basicConfig(level=logging.INFO)

Next trim cutplace's logging to show only warnings and errors as you might not
be particularly interested in whatever it is cutplace does during a
validation:

>>> logging.getLogger("cutplace").setLevel(logging.WARNING)

This should be enough to get you going. To learn more about logging, take a
look at `logging chapter <http://docs.python.org/library/logging.html>`_ of
the Python library documentation.

Reading an ICD
==============

The class
`interface.InterfaceControlDocument <api/cutplace.interface.InterfaceControlDocument-class.html>`_
represents an ICD. In case you have an ICD stored in a file and want to read
it, use:

>>> import os.path
>>> from cutplace import interface
>>>
>>> # Compute the path of a test file in a system independent manner.
>>> icdPath = os.path.join("tests", "input", "icds", "customers.csv")
>>>
>>> icd = interface.InterfaceControlDocument()
>>> icd.read(icdPath)
>>> icd.fieldNames
[u'branch_id', u'customer_id', u'first_name', u'surname', u'gender', u'date_of_birth']

This is the easiest way, which also keeps declaration and validation in
separate files.

Building an ICD in the code
===========================


In some cases it might be preferable to include the ICD in the code, for
instance for trivial interfaces that are only used internally. Here is an
example of a simple ICD for CSV data with 3 fields:

First, import the necessary modules:

>>> from cutplace import data
>>> from cutplace import fields
>>> from cutplace import interface

Next create an empty ICD:

>>> icd = interface.InterfaceControlDocument()

As the ICD will not be read from an input file, error messages would not be
able to refer to any file in case of errors. To have at least some reference,
we need to tell the ICD that it is declared from source code:

>>> icd.setLocationToSourceCode()

That way, error messages will refer you to the Python module where this call
happened.

>>> # Use CSV as data format. This is the same as having a spreadsheet
>>> # with the cells:
>>> #
>>> # | F | Format         | CSV |
>>> # | F | Item separator | ;   |
>>> icd.addDataFormat([data.KEY_FORMAT, data.FORMAT_CSV])
>>> icd.addDataFormat([data.KEY_ITEM_DELIMITER, ";"])
>>>
>>> # Add a couple of fields.
>>> icd.addFieldFormat(["id", "", "", "1:5", "Integer"])
>>> icd.addFieldFormat(["name"])
>>> icd.addFieldFormat(["dateOfBirth", "", "X", "", "DateTime", "YYYY-MM-DD"])
>>>
>>> # Make sure that the `id` field contains only unique values.
>>> icd.addCheck(["id_must_be_unique", "IsUnique", "id"])

>>> icd.fieldNames
['id', 'name', 'dateOfBirth']

If any of this methods cannot handle the parameters you passed, they raise a
``CutplaceError`` with a message describing what went wrong. For example:

>>> icd.addCheck([])
Traceback (most recent call last):
    ...
CheckSyntaxError: <source> (R1C2): check row (marked with 'c') must contain at least 2 columns

Validate data
=============

Once the ICD is set up, you can validate data using ``validate()``:

>>> icdPath = os.path.join("tests", "input", "icds", "customers.csv")
>>> icd = interface.InterfaceControlDocument()
>>> icd.read(icdPath)
>>>
>>> validCsvPath = os.path.join("tests", "input", "valid_customers.csv")
>>> icd.validate(validCsvPath)

So what happens if the data contain errors? Let's give it a try:

>>> brokenCsvPath = os.path.join("tests", "input", "broken_customers.csv")
>>> icd.validate(brokenCsvPath)

Again, the validation runs through without any ``Exception`` or other
indication that something is wrong.

The reason for that is that cutplace should be able to continue in case a data
row is rejected. Raining an ``Exception`` would defeat that. So instead, it
informs interested listeners about validation events. To act on events, define
a class inheriting from ``BaseValidationListener`` and overwrite the methods
for the events you are interested in:

>>> class ErrorPrintingValidationListener(interface.BaseValidationListener):
...     def rejectedRow(self, row, error):
...         print "%r" % row
...         print "error: %s" % error

This is a very simple listener which is only interested about rejected rows. In
case this happens, it simply prints the row and the error that was detected in it.
To learn about other events this listener can receive, take a look at the API
documentation of
`BaseValidationListener <api/cutplace.interface.BaseValidationListener-class.html>`_

To actually get some information about validation errors, you have to create
such a listener and attach it to an ICD:

>>> errorPrintingValidationListener = ErrorPrintingValidationListener()
>>> icd.addValidationListener(errorPrintingValidationListener)

Let's see what happens if we validate broken data again:

>>> icd.validate(brokenCsvPath)
[u'12345', u'92', u'Bill', u'Carter', u'male', u'05.04.1953']
error: broken_customers.csv (R4C1): field u'branch_id' must match format: value u'12345' must match regular expression: u'38\\d\\d\\d'
[u'38111', u'XX', u'Sue', u'Brown', u'female', u'08.02.1962']
error: broken_customers.csv (R5C2): field u'customer_id' must match format: value must be an integer number: u'XX'
[u'38088', u'83', u'Rose', u'Baker', u'female', u'30.02.1994']
error: broken_customers.csv (R6C6): field u'date_of_birth' must match format: date must match format DD.MM.YYYY (%d.%m.%Y) but is: u'30.02.1994' (day is out of range for month)

When you are done, remove the listener::

>>> icd.removeValidationListener(errorPrintingValidationListener)

Putting it all together
=======================

You now know how to:

* declare and ICD in the source code
* validate data from a file
* listen to event happening during validation

All that is left to do is to collect the code snipplets of the previous sections
in one example you can use as base for your own validation code:

>>> # Validate a test CSV file.
>>> import os.path
>>> from cutplace import interface
>>> # Define a listener for validation events.
>>> class ErrorPrintingValidationListener(interface.BaseValidationListener):
...     def rejectedRow(self, row, error):
...         print "%r" % row
...         print "error: %s" % error
>>> # Change this to use your own files.
>>> icdPath = os.path.join("tests", "input", "icds", "customers.csv")
>>> dataPath = os.path.join("tests", "input", "broken_customers.csv")
>>> # Define the interface.
>>> icd = interface.InterfaceControlDocument()
>>> icd.read(icdPath)
>>> # Validate the data.
>>> errorPrintingValidationListener = ErrorPrintingValidationListener()
>>> icd.addValidationListener(errorPrintingValidationListener)
>>> try:
...     icd.validate(brokenCsvPath)
... finally:
...     icd.removeValidationListener(errorPrintingValidationListener)
[u'12345', u'92', u'Bill', u'Carter', u'male', u'05.04.1953']
error: broken_customers.csv (R4C1): field u'branch_id' must match format: value u'12345' must match regular expression: u'38\\d\\d\\d'
[u'38111', u'XX', u'Sue', u'Brown', u'female', u'08.02.1962']
error: broken_customers.csv (R5C2): field u'customer_id' must match format: value must be an integer number: u'XX'
[u'38088', u'83', u'Rose', u'Baker', u'female', u'30.02.1994']
error: broken_customers.csv (R6C6): field u'date_of_birth' must match format: date must match format DD.MM.YYYY (%d.%m.%Y) but is: u'30.02.1994' (day is out of range for month)

Writing field formats
=====================

Cutplace already ships with several field formats found in the `fields
<api/cutplace.fields-module.html>`_ module that should cover most needs If
however you have some very special requirements, you can write your own
formats.

Simply inherit from ``AbstractFieldFormat`` and optionally provide a
constructor to parse the ``rule`` parameter. Next, implement
``validatedValue(self, value)`` that validates that the text in ``value``
conforms to ``rule``. If not, raise an ``FieldValueError`` with a descriptive
error message.

Here is a very simple example of a field format that accepts values of "red",
"green" and "blue".

>>> class ColorFieldFormat(fields.AbstractFieldFormat):
...     def __init__(self, fieldName, isAllowedToBeEmpty, length, rule, dataFormat):
...         super(ColorFieldFormat, self).__init__(fieldName, isAllowedToBeEmpty, length, rule, dataFormat, emptyValue="")
...
...     def validatedValue(self, value):
...         # Validate that ``value`` is a color and return it.
...         assert value
...         if value not in ["red", "green", "blue"]:
...             raise fields.FieldValueError("color value is %r but must be one of: red, green, blue" % value)
...         return value

The ``value`` parameter is a Unicode string. Cutplace ensures that
``validatedValue()`` will never be called with an empty ``value`` parameter,
hence the ``assert value`` - it will cause an ``AssertionError`` if ``value``
is ``""`` or ``None`` because that would mean cutplace is broken.

>>> colorField = ColorFieldFormat("roofColor", False, "", "", icd.dataFormat)
>>> colorField.validated("red")
'red'

Of course you could have achieved similar results using `fields.ChoiceFieldFormat
<api/fields.ChoiceFieldFormat-class.html>`_. However, a custom field format can
do more. In particular, ``validatedValue()`` does not have to return a string.
It can return any Python type and even ``None``. The result will be used in the
``row`` array cutplace sends to any `BaseValidationListener.acceptedRow()
<api/cutplace.interface.BaseValidationListener-class.html#acceptedRow>`_.

Here's a more advanced ``ColorFieldFormat`` that returns the color as a
tuple of RGB items:

>>> class ColorFieldFormat(fields.AbstractFieldFormat):
...     def __init__(self, fieldName, isAllowedToBeEmpty, length, rule, dataFormat):
...         super(ColorFieldFormat, self).__init__(fieldName, isAllowedToBeEmpty, length, rule, dataFormat, emptyValue="")
...
...     def validatedValue(self, colorName):
...         # Validate that ``colorName`` is a color and return its RGB representation.
...         assert colorName
...         if colorName == "red":
...             result = (1.0, 0.0, 0.0)
...         elif colorName == "green":
...             result = (0.0, 1.0, 0.0)
...         elif colorName == "blue":
...             result = (0.0, 1.0, 0.0)
...         else:
...             raise fields.FieldValueError("color name is %r but must be one of: red, green, blue" % colorName)
...         return result

For a simple test, let's see this field format in action:

>>> colorField = ColorFieldFormat("roofColor", False, "", "", icd.dataFormat)
>>> colorField.validated("red")
(1.0, 0.0, 0.0)
>>> colorField.validated("yellow")
Traceback (most recent call last):
...
FieldValueError: color name is 'yellow' but must be one of: red, green, blue

Before you learned that ``validatedValue()`` never gets called with an empty
value. So what happens if you declare a color field that allows empty values,
for instance:

>>> # Sets ``isAllowedToBeEmpty`` to ``True`` to accept empty values.
>>> colorField = ColorFieldFormat("roofColor", True, "", "", icd.dataFormat)
>>> colorField.validated("")
''
>>> # Not quiet a color tuple...

Well, that's not quite what we want. Instead of an empty string, some default
RGB tuple would be a lot more useful. Say, ``(0.0, 0.0, 0.0)`` to represent
black.

Fortunately field formats can just specify that by using the ``emptyValue``
parameter in the constructor. When passed to the ``super`` constructor in
``AbstractFieldFormat``, everything will be taken care of. So here's a
slightly modified version:

>>> class ColorFieldFormat(fields.AbstractFieldFormat):
...     def __init__(self, fieldName, isAllowedToBeEmpty, length, rule, dataFormat):
...         super(ColorFieldFormat, self).__init__(fieldName, isAllowedToBeEmpty, length, rule, dataFormat,
...                 emptyValue=(0.0, 0.0, 0.0)) # Use black as "empty" color.
...
...     def validatedValue(self, colorName):
...         # (Exactly same as before)
...         assert colorName
...         if colorName == "red":
...             result = (1.0, 0.0, 0.0)
...         elif colorName == "green":
...             result = (0.0, 1.0, 0.0)
...         elif colorName == "blue":
...             result = (0.0, 1.0, 0.0)
...         else:
...             raise fields.FieldValueError("color name is %r but must be one of: red, green, blue" % colorName)
...         return result

Let's give it a try:

>>> colorField = ColorFieldFormat("roofColor", True, "", "", icd.dataFormat)
>>> colorField.validated("red")
(1.0, 0.0, 0.0)
>>> colorField.validated("")
(0.0, 0.0, 0.0)

Now that you know how to write your own field format, it would be nice to
actually utilize it in an ICD.

TODO: Describe how to write a ``myfields.py`` and extend the Python path.

Writing checks
==============

Writing checks is quite similar to writing field formats. However, the
interaction with the validation is more complex.

Checks have to implement certain methods described in `checks.AbstractCheck
<api/cutplace.checks.AbstractCheck-class.html>`_. For each check, cutplace
performs the following actions:

#. When reading the ICD, call the check's ``__init__()``.
#. When starting to read a set of data, call the checks's ``reset()``.
#. For each row of data, call the checks's ``checkRow()``.
#. When done with a set of data, call the checks's ``checkAtEnd()``.

The remaineder of this section will describe how to implement each of
these methods. As an example, we implement a check to ensure that
each customer's full name requires less than 100 characters. The field
formats already ensure that ``first_name`` and ``last_name`` are at most
60 characters each. However, assuming the full name is derived using the
expression::

    last_name + ", " + first_name

this could lead to full names with up to 122 characters.

To implements this check, start by inheriting from `checks.AbstractCheck
<api/cutplace.checks.AbstractCheck-class.html>`_:

>>> from cutplace import checks
>>> class FullNameLengthIsInRangeCheck(checks.AbstractCheck):
...     """Check that total length of customer name is within the specified range."""

Next, implement a constructor to which cutplace can pass the values
found in the ICD. For example, for our check the ICD would contain:

+-+-------------------------------------------+------------------------+-----+
+ +Description                                +Type                    +Rule +
+=+===========================================+========================+=====+
+C+full name must have at most 100 characters +FullNameLengthIsInRange +:100 +
+-+-------------------------------------------+------------------------+-----+

When cutplace encounters this line, it will create a new check by calling
``checks.FullNameLengthIsInRangeCheck.__init__()``, passing the following
parameters:

* ``description="customer must be unique"``, which is just a human readable
  description of the check to refer to it in error messages
* ``rule=":100"``, which describes what exactly the check
  should do. Each check can define its own syntax for the rule. In case of
  ``FullNameLengthIsInRange`` the rule describes a `ranges.Range <api/cutplace.ranges.Range-class.html>`_.
* ``availableFieldNames=["branch_id", "customer_id", "first_name","last_name",
  "gender", "date_of_birth"]`` (as defined in the ICD and using the same order)
* ``location`` being the ``tools.InputLocation`` in the ICD where the check was defined.

The constructor basically has to do 3 things:

#. Call the super constructor
#. Perform optional initialisation needed by the check that needs to be
   done only once and not on each new data set. In most cases, this involves
   parsing the ``rule`` parameter and obtain whatever information the checks needs
   from it.
#. Call ``self.reset()``. This is not really necessary for this check, but in most
   cases it will make your life easier because you can avoid redundant initialisations
   in the constructor.

>>> from cutplace import ranges
>>> class FullNameLengthIsInRangeCheck(checks.AbstractCheck):
...     """Check that total length of customer name is within the specified range."""
...     def __init__(self, description, rule, availableFieldNames, location=None):
...         super(FullNameLengthIsInRangeCheck, self).__init__(description, rule, availableFieldNames, location)
...         self._fullNameRange = ranges.Range(rule)
...         self.reset()

Once cutplace is done reading the ICD, it moves on to data. For each set of
data it calls the checks `reset()
<api/cutplace.checks.AbstractCheck-class.html#reset>`_ method. For our simple
check, no actions are needed so we are good already because ``AbstractCheck``
already provides a ``reset()`` that does nothing.

When cutplace validates data, it reads them row by row. For each row, it
calls `validated() <api/cutplace.fields.AbstractFieldFormat-class.html#validated>`_
on each cell in the row. In case all cells are valid, it collects them in a
dictionary which maps the field name to its native value. Recall the interface
from the :doc:`tutorial`, which defined the following fields:

+-+--------------------+----------+------+------+--------+------------+
+ +Name                +Example   +Empty?+Length+Type    +Rule        +
+=+====================+==========+======+======+========+============+
+F+branch_id           +38000     +      +5     +        +            +
+-+--------------------+----------+------+------+--------+------------+
+F+customer_id         +16        +      +2:    +Integer +10:65535    +
+-+--------------------+----------+------+------+--------+------------+
+F+first_name          +Jane      +      +:60   +        +            +
+-+--------------------+----------+------+------+--------+------------+
+F+surname             +Doe       +      +:60   +        +            +
+-+--------------------+----------+------+------+--------+------------+
+F+gender              +female    +      +2:6   +Choice  +male, female+
+-+--------------------+----------+------+------+--------+------------+
+F+date_of_birth       +27.02.1946+X     +10    +DateTime+DD.MM.YYYY  +
+-+--------------------+----------+------+------+--------+------------+

Now consider a data row with the following values:

+---------+-----------+----------+-------+------+-------------+
+Branch id+Customer id+First name+Surname+Gender+Date of birth+
+=========+===========+==========+=======+======+=============+
+38111    +96         +Andrew    +Dixon  +male  +02.10.1913   +
+---------+-----------+----------+-------+------+-------------+

The row map for this row would be::

  rowMap = {
      "branch_id": 38111,
      "customer_id": 96,
      "first_name": "Andrew",
      "last_name": "Dixon",
      "gender": "male",
      "date_of_birth": time.struct_time(tm_year=1913, tm_mon=10, tm_mday=2, ...)
  }

With this knowledge, we can easily implement a ``checkRow`` that computes the
full name and checks that it is within the required range. If not, it raises
a `CheckError <api/cutplace.checks.CheckError-class.html>`_:

>>> def checkRow(self, rowMap, location):
...     fullName = rowMap["last_name"] + ", " + rowMap["first_name"]
...     fullNameLength = len(fullName)
...     try:
...         self._fullNameRange.validate("full name", fullNameLength)
...     except ranges.RangeValueError, error:
...         raise CheckError("full name length is %d but must be in range %s: %r" \
...                 % (fullNameLength, self._fullNameRange, fullName))

And finally, there is
`checkAtEnd() <api/cutplace.checks.AbstractCheck-class.html#checkAtEnd>`_ which
is called when all data rows have been processed. Note that ``checkAtEnd()``
does not have any parameters that contain actual data. Instead you typically
would collect all information needed by ``checkAtEnd()`` in ``checkRow()`` and
store them in instance variables.

Because our ``FullNameLengthIsInRangeCheck`` does not need to do anything here,
we can omit it and keep inherit an empty implementation from ``AbstractCheck``.

TODO: Describe how to write mychecks.py and extend Python path.
