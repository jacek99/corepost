'''
Enhancements to core Twisted security
@author: jacekf
'''

from twisted.cred.checkers import ICredentialsChecker, FilePasswordDB
from zope.interface import implements

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class CachedCredentialsChecker:
    """A cached credentials checker wrapper. It will forward calls to the actual credentials checker only when the cache expires (or on first call)"""
    implements(ICredentialsChecker)
    
    def __init__(self,credentialInterfaces,credentialsChecker):
        self.credentialInterfaces = credentialInterfaces
        self.checker = credentialsChecker

    def requestAvatarId(self,credentials):
        pass

class SqlCredentialsChecker:
    """A SQL checked to compare usernames and passwords to a DB table, with support for custom comparison (plaintext, hash, etc)"""
    implements(ICredentialsChecker)
    
    def __init__(self,dbpool,userTable,usernameColumn,passwordColumn,passwordChecker = None):
        """Constructor
        @param dbpool: adbapi DB connection pool
        @param userTable: Name of the table containing list of users
        @param userameColumn: Name of column containing the user name
        @param passwordColumn: Name of column containing the user password (or its hash)
        @param passwordChecker: A lambda that compares the incoming password due what is stored in DB (plaintext comparison (not recommended, insecure), hash, decryption, etc.)
        """
        self.dbpool = dbpool
        self.userTable = userTable
        self.usernameColumn = usernameColumn
        self.passwordColumn = passwordColumn
        self.passwordChecker = passwordChecker

    def requestAvatarId(self,credentials):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
        
    
    