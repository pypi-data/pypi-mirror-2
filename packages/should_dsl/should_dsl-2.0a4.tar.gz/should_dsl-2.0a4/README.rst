Should-DSL: Improve readability for should-style expectations
=============================================================

The goal of *Should-DSL* is to write should expectations in Python as clear and readable as possible, using **"almost"** natural language (limited - sometimes - by the Python language constraints).

For using this DSL, you need to import the should and should_not objects from should_dsl module, or import all from should_dsl.

For example::

    >>> from should_dsl import should

    >>> 1 |should| equal_to(1)
    >>> 'should' |should| include('oul')
    >>> 3 |should| be_into([0, 1, 2])
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 3 is not into [0, 1, 2]


The *equal_to* matcher verifies object equality. If you want to ensure identity, you must use *be* as matcher::

    >>> 2 |should| be(2)


A nice example of exceptions would be::

    >>> def raise_zerodivisionerror():
    ...     return 1/0
    >>> raise_zerodivisionerror |should| throw(ZeroDivisionError)


*should* has a negative version::

    >>> from should_dsl import should_not

    >>> 2 |should_not| be_into([1, 3, 5])
    >>> 'should' |should_not| include('oul')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 'should' does include 'oul'



Should-DSL Matchers
===================

Below there are some explanations about the available matchers in *should_dsl* package.


Available Matchers
------------------


**be**

Checks object identity (*is*).

::

    >>> 1 |should| be(1)

    >>> a = "some message"
    >>> b = "some message"
    >>> id(a) == id(b) # the strings are equal but the ids are different
    False
    >>> a |should| be(b)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 'some message' is not 'some message'

    >>> c = "another message"
    >>> d = c
    >>> id(c) == id(d)
    True
    >>> c |should| be(d)


**be_greater_than**

**be_greater_than_or_equal_to**

**be_less_than**

**be_less_than_or_equal_to**

Simply checks the given comparisons.

::

    >>> 1 |should_not| be_greater_than(1)

    >>> 2 |should| be_greater_than_or_equal_to(2)

    >>> 0.1 |should| be_less_than(0.11)

    >>> 3000 |should| be_less_than_or_equal_to(3001)


**be_into**

**contain**

**include**

Verifies if an object is contained (*be_into*) or contains (*contain*) another. The *contain* and *include* matchers do exactly the same job.

::

    >>> 1 |should| be_into(range(2))

    >>> ['a'] |should_not| be_into(['a'])

    >>> ['a'] |should| be_into([['a']])

    >>> ['x', 'y', 'z'] |should| contain('z')

    >>> ['x', 'y', 'z'] |should| include('z')


**be_kind_of**

Verifies if an object is of a given type.

::

    >>> 1 |should| be_kind_of(int)

    >>> class Foo: pass
    >>> Foo() |should| be_kind_of(Foo)

    >>> class Bar(Foo): pass
    >>> Bar() |should| be_kind_of(Foo)

**be_instance_of**

Like be_kind_of, but it uses *instance* word.


**be_like**

Checks matching against a regular expression.

::

    >>> 'Hello World' |should| be_like(r'Hello W.+')

    >>> '123 is a number' |should_not| be_like(r'^[12]+ is a number')


**be_thrown_by**

**throw**

Checks if a given piece of code raises an arbitrary exception.

::

    >>> ZeroDivisionError |should| be_thrown_by(lambda: 1/0)

    >>> (lambda: 1/0.000001) |should_not| throw(ZeroDivisionError)

*throw* matcher also supports message checking.

::

    >>> def foo():
    ...     raise TypeError("Hey, it's cool!")

    >>> foo |should| throw(TypeError("Hey, it's cool!"))

    >>> foo |should| throw(TypeError("This won't work..."))
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected to throw 'TypeError' with the message "This won't work...", got 'TypeError' with "Hey, it's cool!"

    Or you can use ``message`` parameter to throw, like
    >>> foo |should| throw(TypeError, message= "Hey, it's cool!")


If the function or method has parameters, it must be called within a lambda or using a tuple. The following ways are both equivalent::

    >>> def divide(x, y): return x / y

    >>> (lambda: divide(1, 0)) |should| throw(ZeroDivisionError)

    >>> (divide, 1, 0) |should| throw(ZeroDivisionError)

The same works for *be_thrown_by* matcher.


**change**

Checks for changes on the result of a given function, method or lambda.

::

    >>> class Box(object):
    ...     def __init__(self):
    ...         self.items = []
    ...     def add_items(self, *items):
    ...         for item in items:
    ...             self.items.append(item)
    ...     def item_count(self):
    ...         return len(self.items)
    ...     def clear(self):
    ...         self.items = []
    >>> box = Box()
    >>> box.add_items(5, 4, 3)

    >>> box.clear |should| change(box.item_count)

    >>> box.clear |should_not| change(box.item_count)

If the function or method has parameters, it must be called within a lambda or using a tuple. The following ways are both equivalent::

    >>> (lambda: box.add_items(1, 2, 3)) |should| change(box.item_count)

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count)

*change* also works given an arbitrary change count::

    >>> box.clear()
    >>> box.add_items(1, 2, 3)
    >>> box.clear |should| change(box.item_count).by(-3)

    >>> box.add_items(1, 2, 3)
    >>> box.clear |should| change(box.item_count).by(-2)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by -2, but was changed by -3

*change* has support for maximum and minumum with *by_at_most* and *by_at_least*::

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(3)

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_most(2)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by at most 2, but was changed by 3

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(3)

    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).by_at_least(4)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have changed by at least 4, but was changed by 3


And, finally, *change* supports specifying the initial and final values or only the final one::

    >>> box.clear()
    >>> (box.add_items, 1, 2, 3) |should| change(box.item_count).from_(0).to(3)

    >>> box.clear |should| change(box.item_count).to(0)

    >>> box.clear |should| change(box.item_count).to(0)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: result should have been changed to 0, but is now 0



**close_to**

Checks if a number is close to another, given a delta.

::

    >>> 1 |should| close_to(0.9, delta=0.1)

    >>> 0.8 |should| close_to(0.9, delta=0.1)

    >>> 1 |should_not| close_to(0.89, delta=0.1)

    >>> 4.9 |should| close_to(4, delta=0.9)


**end_with**

Verifies if a string ends with a given suffix.

::

    >>> "Brazil champion of 2010 FIFA world cup" |should| end_with('world cup')

    >>> "hello world" |should_not| end_with('worlds')


**equal_to**

Checks object equality (not identity).

::

    >>> 1 |should| equal_to(1)

    >>> class Foo: pass
    >>> Foo() |should_not| equal_to(Foo())

    >>> class Foo(object):
    ...     def __eq__(self, other):
    ...         return True
    >>> Foo() |should| equal_to(Foo())


**equal_to_ignoring_case**

Checks equality of strings ignoring case.

::

    >>> 'abc' |should| equal_to_ignoring_case('AbC')

    >>> 'XYZAb' |should| equal_to_ignoring_case('xyzaB')


**have**

Checks the element count of a given collection. It can work with iterables, requiring a qualifier expression for readability purposes that is only a syntax sugar.

::

    >>> ['b', 'c', 'd'] |should| have(3).elements

    >>> [1, [1, 2, 3], 'a', lambda: 1, 2**3] |should| have(5).heterogeneous_things

    >>> ['asesino', 'japanische kampfhoerspiele', 'facada'] |should| have(3).grindcore_bands

    >>> "left" |should| have(4).characters

*have* also works with non-iterable objects, in which the qualifier is a name of attribute or method that contains the collection to be count.

::

    >>> class Foo:
    ...     def __init__(self):
    ...         self.inner_things = ['a', 'b', 'c']
    ...     def pieces(self):
    ...         return range(10)
    >>> Foo() |should| have(3).inner_things

    >>> Foo() |should| have(10).pieces


*have* supports the checking of element count of an iterable within an attribute of an object. This feature works for both attributes and functions.

::

    >>> class Team:
    ...     def __init__(self, total_player_count, starting_count):
    ...         self.players = list(range(total_player_count))
    ...         self._starting_count = starting_count
    ...     def starting_players(self):
    ...         return self.players[:self._starting_count]

    >>> class Club:
    ...     def __init__(self, team):
    ...         self.team = team
    ...     def winner_team(self):
    ...         return self.team

    >>> football_team = Team(22, 11)
    >>> handball_team = Team(14, 7)
    >>> flamengo = Club(football_team)
    >>> metodista = Club(handball_team)

    >>> flamengo |should| have(22).players_on_team
    >>> flamengo |should| have(11).starting_players_on_winner_team

    >>> metodista |should| have(14).players_on_winner_team
    >>> metodista |should| have(7).starting_players_on_team


**have_at_least**

Same to *have*, but checking if the element count is greater than or equal to the given value. Works for collections with syntax sugar, object attributes or methods.

::

    >>> range(20) |should| have_at_least(19).items

    >>> range(20) |should| have_at_least(20).items

    >>> range(20) |should_not| have_at_least(21).items


**have_at_most**

Same to *have*, but checking if the element count is less than or equal to the given value. Works for collections with syntax sugar, object attributes or methods.

::

    >>> range(20) |should_not| have_at_most(19).items

    >>> range(20) |should| have_at_most(20).items

    >>> range(20) |should| have_at_most(21).items



**include_all_of**

**include_in_any_order**

Check if a iterable includes all elements of another. Both matchers do the same job.

::

   >>> [4, 5, 6, 7] |should| include_all_of([5, 6])

   >>> [4, 5, 6, 7] |should| include_in_any_order([5, 6])

   >>> ['b', 'c'] |should| include_all_of(['b', 'c'])

   >>> ['b', 'c'] |should| include_in_any_order(['b', 'c'])

   >>> ['b', 'c'] |should_not| include_all_of(['b', 'c', 'a'])

   >>> ['b', 'c'] |should_not| include_in_any_order(['b', 'c', 'a'])



**include_any_of**

Checks if an iterable includes any element of another.

::

    >>> [1, 2, 3] |should| include_any_of([3, 4, 5])

    >>> (1,) |should| include_any_of([4, 6, 3, 1, 9, 7])



**respond_to**

Checks if an object has a given attribute or method.

::

    >>> 'some string' |should| respond_to('startswith')


    >>> class Foo:
    ...     def __init__(self):
    ...         self.foobar = 10
    ...     def bar(self): pass

    >>> Foo() |should| respond_to('foobar')

    >>> Foo() |should| respond_to('bar')



**start_with**

Verifies if a string starts with a given prefix.

::

    >>> "Brazil champion of 2010 FIFA world cup" |should| start_with('Brazil champion')

    >>> "hello world" |should_not| start_with('Hello')



Predicate matchers
------------------

Should-DSL supports predicate matchers::

    >>> class Foo(object):
    ...     def __init__(self, valid=True):
    ...         self.valid = valid

    >>> Foo() |should| be_valid

By default predicate matchers look for the exact attribute/metod name.
In the previous example, it looks for ``valid`` attribute or method.
Should-DSL looks for ``is_valid`` and ``isvalid`` if ``valid`` was not found.

::

    >>> class Integer(int):
    ...     def __init__(self, value):
    ...         self.is_negative = value < 0
    ...         self.isodd = (value % 2 == 1) 
    >>> Integer(-1) |should| be_negative
    >>> Integer(1) |should| be_odd


Predicate matchers also work with methods::

    >>> class House(object):
    ...     def __init__(self, kind):
    ...         self._kind = kind
    ...     def made_of(self, kind):
    ...         return self._kind.upper() == kind.upper()
    >>> house = House('Wood')

    >>> house |should| be_made_of('wood')

    >>> house |should| be_made_of('stone')
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected made_of('stone') to return True, got False


And it is possible to customize how Should-DSL find matchers, using ``add_predicate_regex``::

    >>> from should_dsl import add_predicate_regex
    >>>
    >>> add_predicate_regex(r'is_really_(.+)')
    >>> class Integer(int):
    ...     def __init__(self, value):
    ...         self.is_really_positive = value >= 0
    >>> Integer(10) |should| be_positive

This last example tells Should-DSL when someone uses ``be_SOMENAME``,
it should look for attribute or method named ``is_really_SOMENAME``.

Custom matchers
---------------

Extending the DSL with custom matchers is very easy. For simple matchers, a decorated function is enough. The function name must be the name of the matcher. The function must have no parameters and it must return a tuple containing two elements. The first one is the function (or lambda), receiving two parameters, to be run for the comparison, and the second is the failure message. The failure message must have three %s placeholders. The first and the third for, respectively, the actual and expected values. Second %s is a placeholder for a 'not ' string for a failed should_not, or an empty string for a failed should. In the example, when should fails, a message can be "4 is not the square root of 9"; in another way, if the fail is in a should_not, the message could be "3 is the square root of 9", if the expectation was *3 \|should_not\| be_the_square_root_of(9)*. The example is below::

    >>> from should_dsl import matcher

    >>> @matcher
    ... def be_the_square_root_of():
    ...     import math
    ...     return (lambda x, y: x == math.sqrt(y), "%s is %sthe square root of %s")

    >>> 3 |should| be_the_square_root_of(9)

    >>> 4 |should| be_the_square_root_of(9)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: 4 is not the square root of 9


If your custom matcher has a more complex behaviour, or if both should and should_not messages differ, you can create custom matchers as classes. In fact, classes as matchers are the preferred way to create matchers, being function matchers only a convenience for simple cases.

Below is an example of the square root matcher defined as a class::

    >>> import math
    >>> class SquareRoot(object):
    ...
    ...     name = 'be_the_square_root_of'
    ...
    ...     def __call__(self, radicand):
    ...         self._radicand = radicand
    ...         return self
    ...
    ...     def match(self, actual):
    ...         self._actual = actual
    ...         self._expected = math.sqrt(self._radicand)
    ...         return self._actual == self._expected
    ...
    ...     def message_for_failed_should(self):
    ...         return 'expected %s to be the square root of %s, got %s' % (
    ...             self._actual, self._radicand, self._expected)
    ...
    ...     def message_for_failed_should_not(self):
    ...         return 'expected %s not to be the square root of %s' % (
    ...             self._actual, self._radicand)
    ...
    >>> matcher(SquareRoot)
    <class ...SquareRoot...>

    >>> 3 |should| be_the_square_root_of(9)

    >>> 4 |should| be_the_square_root_of(9)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected 4 to be the square root of 9, got 3.0

    >>> 2 |should_not| be_the_square_root_of(4.1)

    >>> 2 |should_not| be_the_square_root_of(4)
    Traceback (most recent call last):
    ...
    ShouldNotSatisfied: expected 2 not to be the square root of 4


PS.: If you use Python2.6 you can use the class decorator (just a syntax sugar)::

    @matcher
    class SquareRoot(object):
        # the same body here

    instead of

    class SquareRoot(object):
        # body
    matcher(SquareRoot)


A matcher class must fill the following requirements:

- a class attribute called *name* containing the desired name for the matcher;
- a *match(actual)* method receiving the actual value of the expectation as a parameter (e.g., in
  *2 \|should\| equal_to(3)* the actual is 2 and the expected is 3). This method should return
  the boolean result of the desired comparison;
- two methods, called *message_for_failed_should* and *message_for_failed_should_not* for returning
  the failure messages for, respectively, should and should_not.

The most common way the expected value is inject to the matcher is through making the matcher
callable. Thus, the matcher call can get the expected value and any other necessary or optional
information. By example, the *close_to* matcher's *__call__()* method receives 2 parameters:
the expected value and a delta. Once a matcher is a regular Python object, any Python can be used.
In *close_to*, delta can be used as a named parameter for readability purposes.


Deprecated usage
----------------

All *should-dsl* matchers also support a deprecated form, so::

    >>> 3 |should_not| equal_to(2.99)


can be written as::

    >>> 3 |should_not.equal_to| 2.99


Besides, should_dsl module offers should_be, should_have (and their negative counterparts) to be used with no matchers, as::

    >>> from should_dsl import *

    >>> [1, 2] |should_have| 1

    >>> 1 |should_be| 1


This syntax for writing expectations was changed because the requirement to have a single "right value" is a limitation to future improvements.

We don't plan to remove the deprecated syntax in the near future, but we discourage its use from now.



Should-DSL with unittest
========================

*should-dsl* is unittest-compatible, so, on a unittest test case, failures on should expectations will result on unittest failures, not errors::

    >>> from should_dsl import *
    >>> import os
    >>> import unittest

    >>> class UsingShouldExample(unittest.TestCase):
    ...     def test_showing_should_not_be_works(self):
    ...         'hello world!' |should_not| be('Hello World!')
    ...
    ...     def test_showing_should_include_fails(self):
    ...         [1, 2, 3] |should| include(5)
    ...
    ...     def test_showing_should_include_works(self):
    ...         'hello world!' |should| include('world')
    ...
    ...     def test_showing_should_not_include_fails(self):
    ...         {'one': 1, 'two': 2} |should_not| include('two')
    ...
    ...     def test_showing_should_not_include_works(self):
    ...         ["that's", 'all', 'folks'] |should_not| include('that')

    >>> devnull = open(os.devnull, 'w')
    >>> runner = unittest.TextTestRunner(stream=devnull)
    >>> suite = unittest.TestLoader().loadTestsFromTestCase(UsingShouldExample)
    >>> runner.run(suite)
    <unittest...TextTestResult run=5 errors=0 failures=2>
    >>> devnull.close()

