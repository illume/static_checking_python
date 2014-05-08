
def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Pylint does not find this, However PyCharm does find it.
    return "The duck quacked this many times:" + 2

doduck()
