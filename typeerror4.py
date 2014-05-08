import typeerrorsupport

def doduck():
    # This will give a TypeError: cannot concatenate 'str' and 'int' objects
    # Neither PyCharm, or pylint find this.
    return "The duck quacked this many times:{}".format(typeerrorsupport.a)

doduck()
