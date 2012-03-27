'''
Enhancements to core Twisted security
@author: jacekf
'''

from twisted.cred.checkers import ICredentialsChecker
from zope.interface import implements

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

class Principal:
    '''A security principal with privileges attached to it'''
    def __init__(self,userId,privileges=None):
        '''
        @param userId -- mandatory user ID
        @param privileges -- list of privileges assigned to this user
        '''
        self.__userId = userId
        self.__privileges = privileges
        
    @property
    def userId(self):
        return self.__userId

    @property
    def privileges(self):
        return self.__privileges

class CachedCredentialsChecker:
    """A cached credentials checker wrapper. It will forward calls to the actual credentials checker only when the cache expires (or on first call)"""
    implements(ICredentialsChecker)
    
    def __init__(self,credentialInterfaces,credentialsChecker):
        self.credentialInterfaces = credentialInterfaces
        self.checker = credentialsChecker
        
        #initialize cache
        cacheOptions = {
            'cache.type': 'memory',
        }
        self.cache = CacheManager(**parse_cache_config_options(cacheOptions))

    def requestAvatarId(self,credentials):
        pass

    
##################################################################################################
#
# DECORATORS
#
##################################################################################################    

def secured(privileges=None):
    '''
    Main decorator for securing REST endpoints via roles
    '''
    pass    
    
    
    
    
    
    
    
    
    
        
    
    