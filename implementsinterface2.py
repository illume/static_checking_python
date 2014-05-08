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
