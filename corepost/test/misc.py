'''
Created on 2011-09-02

Misc tests
@author: jacekf
'''

def dec(f):
    print "DEC"
    def wrap():
        print "WRAP"
        v = f()
        return v
    return wrap


@dec
def test():
    print "TEST3232"

if __name__ == "__main__":
    test()
    test()
    test()