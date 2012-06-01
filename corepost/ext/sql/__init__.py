'''
Multicore module

@author: jacekf
'''

try:
    import txZMQ
except ImportError as ex:
    print "You need to have txZMQ and ZeroMQ installed in order to use multicore support in Corepost"
    raise ex

