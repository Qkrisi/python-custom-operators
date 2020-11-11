CustomOperators
===============

This module allows you to use operators specified by you.

Setup
-----

To install the module, run: ``sudo pip3 install CustomOperators``

Usage
-----

To import the module, use

.. code:: py

    import CustomOperators

To create an operator, use the ``CustomOperators.Operator`` decorator

Examples:

**2 operands:**

.. code:: py

    import CustomOperators

    @CustomOperators.Operator("§")
    def Power(left, right):
        return left**right

**1 operand:**

.. code:: py

    import customOperators

    @CustomOperators.Operator("!")
    def Negate(base):
        return not base

To run a script that uses the new operators, import it with
``CustomOperators.ImportModule``

Example:

.. code:: py

    #Module.py

    def run():
        print(4§5)

.. code:: py

    #__main__.py

    import CustomOperators

    @CustomOperators.Operator("§")
    def Power(left, right):
        return left**right

    CustomOperators.ImportModule("Module")
    Module.run()    #Output: 1024

**For more information about usage (operator overloading, operator
rules), check out the** `wiki
page <https://github.com/Qkrisi/python-custom-operators/wiki>`__
