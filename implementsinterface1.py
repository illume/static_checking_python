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

