Python is considered a strongly typed and dynamically typed language.  Most of its type checking is done at compile time.

So, does that mean Python is also not a statically typed language?  Can python do type checking at compile time?

Yes, Python can be type checked somewhat at compile time.

There are tools to optionally statically type check your python programs.  Unfortunately many people do not realise this when they want it.  It's also used by some people to justify their choices of technology.  In certain situations static typing can be useful, as limiting the expressiveness of your programs can help avoid bugs at compile time.

If you have 100% unit test coverage of your code, shouldn't that catch all the same bugs?  Yes, it probably would.  However, not all teams have 100% branch coverage checking of all their code.

But what exactly are the benefits of static type checking? Each different type system can provide a number of different benefits.

* implements an interface
* compatible operators used on variables, eg "asdf" + 2
* correct number of arguments passed
* unused variables, or modules
* assigned but never used
* lookup the type of a variable
* finding usages of functions
* refactoring

There's hundreds more things you can check for with tools like pylint and some of the IDEs. That 'implements an interface' one is important. Since with interfaces you can specify things like return types, and type arguments. There are also field list markers in doc strings, where you can specify argument and return types. These can be used by tools like IDEs (eg pycharm) and other static checkers. Full program type inference is now doable for large parts of python. See the shedskin, and Rpython restricted subsets for two implementations.

Can you do format proofs of your python programs, and discover things like if they will provably finish, and that they will complete in bounded time, or use under a certain amount of memory?  I'm not sure.

Now I will go over some of these problems and give examples of how you can statically check for them.  I will show which tools work, and which tools do not work for these problems.


# Implements an interface

## implementsinterface1.py

```python

import abc


class Birds(object):
    """docstring for Birds"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, arg):
        self.arg = arg

    @abc.abstractmethod
    def noise(self):
        """docstring for noise"""
        pass

    @abc.abstractmethod
    def move(self):
        """docstring for move"""
        pass


class Duck(Birds):
    """docstring for Duck"""
    __implements__ = (Birds, )
    def __init__(self, arg):
        super(Duck, self).__init__(arg)

    def noises(self):
        """docstring for noise"""
        print self.arg

    def moves(self):
        """docstring for move"""
        print self.arg


class Pidgeon(Birds):
    """docstring for Pidgeon"""
    __implements__ = (Birds, )
    def __init__(self, arg):
        super(Pidgeon, self).__init__(arg)

    def noises(self):
        """docstring for noise"""
        print self.arg


    def moves(self):
        """docstring for move"""
        print self.arg

```
 
```
(anenv)shit-robot:staticchecking rene$ pylint implementsinterface1.py 
No config file found, using default configuration
************* Module implementsinterface1
C:  1, 0: Missing module docstring (missing-docstring)
W: 23, 0: Method 'move' is abstract in class 'Birds' but is not overridden (abstract-method)
W: 23, 0: Method 'noise' is abstract in class 'Birds' but is not overridden (abstract-method)
W: 38, 0: Method 'move' is abstract in class 'Birds' but is not overridden (abstract-method)
W: 38, 0: Method 'noise' is abstract in class 'Birds' but is not overridden (abstract-method)
```


## implementsinterface2.py


Here pylint can find that we are correctly implemented the required methods.


```python

"""docstring for the module
"""
import abc


class Birds(object):
    """docstring for Birds"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, arg):
        self.arg = arg

    @abc.abstractmethod
    def noise(self):
        """docstring for noise"""
        raise NotImplementedError

    @abc.abstractmethod
    def move(self):
        """docstring for move"""
        raise NotImplementedError


class Duck(Birds):
    """docstring for Duck"""
    __implements__ = (Birds, )
    def __init__(self, arg):
        super(Duck, self).__init__(arg)

    def noise(self):
        """docstring for noise"""
        # This will give a TypeError: cannot concatenate 'str' and 'int' objects
        # Pylint does not find this.
        print "a duck quacks this many times:" + 2

    def move(self):
        """docstring for move"""
        print self.arg


class Pidgeon(Birds):
    """docstring for Pidgeon"""
    __implements__ = (Birds, )
    def __init__(self, arg):
        super(Pidgeon, self).__init__(arg)

    def noise(self):
        """docstring for noise"""
        print self.arg


    def move(self):
        """docstring for move"""
        print self.arg
```


# Detecting TypeErrors

Can you check for type errors?  Let us test it out.

## typeerror1.py

```python

def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Pylint does not find this, However PyCharm does find it.
    return "The duck quacked this many times:" + 2

doduck()
```

First we try something simple... adding a string to a number.

This will give a TypeError: cannot concatenate 'str' and 'int' objects

Pylint does not find this error.

However, PyCharm shows the error.  It says "Expected type 'str | unicode', got 'int' instead."

Note that pylint found these problems with the code:

```
(anenv)shit-robot:staticchecking rene$ pylint typeerror2.py 
No config file found, using default configuration
************* Module typeerror2
C:  7, 0: Final newline missing (missing-final-newline)
C:  1, 0: Missing module docstring (missing-docstring)
C:  1, 0: Invalid constant name "a" (invalid-name)
C:  3, 0: Missing function docstring (missing-docstring)
```



## typeerror2.py

```python
a = 2

def doduck():

    return "The duck quacked this many times:" + a

doduck()
```

We make it a bit more complicated for PyCharm, by putting the number into a variable.

Luckily, PyCharm still finds the error.

pylint still can not find this error.


## typeerror3.py

```python
import typeerrorsupport

def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Neither PyCharm, or pylint find this.
    return "The duck quacked this many times:" + typeerrorsupport.a

doduck()
```

Now we move the variable into a separate module.

This is where PyCharm does not find the error.

However pysonar2 can find the return type of the doduck() function is either a string or an int.

pysonar2 is not actually a tool for checking types, but only does the type inference in a library.  It is meant for integrating into IDEs and such.  It does advanced type inference in python.

Here it guesses that it could either return a string or an int type.


The command I used to generate some html output from all the files.  I had installed and compiled 
```
java -jar pysonar2/target/pysonar-2.0-SNAPSHOT.jar . ./html
```

Follow the install instructions at the pysonar2 github page: https://github.com/yinwang0/pysonar2


## typeerror4.py

```python
import typeerrorsupport

def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Neither PyCharm, or pylint find this.
    return "The duck quacked this many times:{}".format(typeerrorsupport.a)

doduck()
```

This is correctly using the format method of string to put the int into the string.

Here pysonar2 correctly sees that an int is returned by the doduck() function.


## typeerror5.py

```python
import typeerrorsupport

def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Neither PyCharm, or pylint find this.
    return "The duck quacked this many times:{}" + typeerrorsupport.number_of_quacks()

doduck()
```


By adding the return type into the doc string of the typeerrorsupport.number_of_quacks() function
we see that PyCharm can detect the TypeError.

If you follow the reST field lists, PyCharm (and other tools) can use that type information.

You can see the field lists here: http://sphinx-doc.org/domains.html#info-field-lists

## typeerrorsupport.py

```python
a = 2

def number_of_quacks():
    """
    :rtype : int
    """
    return 2
```

The docstring tells it, that it would return an int type, and PyCharm detected this across module boundaries.

Note that pylint does not currently detect the TypeError even though we have told it the return type is int via the doctstring field list.


## Conclusion

Much static type checking can be done in a dynamically typed language like python with modern tools.

Whilst none of the tools are perfect by themselves, we can see that by using a combination of the tools we can detect all of the problems we set out to detect.

You can use either the Abstract Base Class in the abc package which comes with python, or zope.interfaces to implement interfaces which can check that interfaces are implemented for you.  I haven't gone into much detail here, just showed some basic interface checking with pylint.  There is much more you can do.

PyCharm combined with appropriately written and typed doc strings can detect many problems.  PyCharm also has many refactoring tools built in, and things like code completion for a dynamically typed language.  Note, that this is not the only IDE or tool for python that can do this, but just the one I'm using for illustration purposes.

pysonar2 shows that types can be inferred without even specifying the types in docstrings.  This has already been shown with tools like shedskin, and RPython(by pypy) which are statically inferring types from a subset of python.  This style of type inference could be used for Ahead of Time (AOT) compilation, and within IDEs for better type inference.  Better type inference allows better type checking, refactoring, and type inspection.
