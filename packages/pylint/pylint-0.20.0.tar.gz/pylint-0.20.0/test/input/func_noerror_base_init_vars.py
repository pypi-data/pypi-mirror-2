# pylint:disable-msg=R0201
"""Checks that class variables are seen as inherited !
"""
__revision__ = ''

class BaseClass:
    """A simple base class
    """
    
    def __init__(self):
        self.base_var = {}

    def met(self):
        """yo"""
    def meeting(self, with_):
        """ye"""
        return with_
class MyClass(BaseClass):
    """Inherits from BaseClass
    """

    def __init__(self):
        BaseClass.__init__(self)
        self.var = {}

    def met(self):
        """Checks that base_var is not seen as defined outsite '__init__'
        """
        self.var[1] = 'one'
        self.base_var[1] = 'one'
        print self.base_var, self.var

if __name__ == '__main__':
    OBJ = MyClass()
    OBJ.met()

