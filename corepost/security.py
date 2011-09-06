'''
Stand-alone security module with support for role-based authorization and IP address range checking
@author: jacekf
'''

from IPy import IP

class SecurityRole:
    '''Represents a security role'''
    def __init__(self,roleId,ipRanges=None):
        '''
        roleId -- role roleId
        ipRanges -- list of ipRanges in any of the formats accepted by the IPy library
        '''
        self.__roleId = roleId
        self.__ipRanges = ipRanges
        
    @property
    def roleId(self):
        return self.__roleId
        
class Principal:
    '''An enhanced Avatar with roles & IP Address ranges attached to it'''
    def __init__(self,userId,roles=None,ipRanges=None):
        '''
        userId -- mandatory user ID
        roles -- list of optional SecurityRole instances
        ipRanges - user-specific IP ranges (checked before the role ones)
        '''
        self.__userId = userId
        self.__roles = roles
        self.__ipRanges = ipRanges
        
    @property
    def userId(self):
        return self.__userId
    
    def validateAccess(self,expectedRoles,ipAddress):
        '''
        Validates if the current Principal has access to any of the expected roles, coming from the current request IP address
        '''
        pass 
        
class SqlCredentialsFactory:
    '''A default credentials factory configured to obtain credentials / roles / IP address ranges via custom SQL queries'''
    def __init__(self,
                 dbConnectionPool,userQuery="SELECT USER_ID FROM USER",
                 userIpRangeQuery = "SELECT IP_RANGE FROM USER_IP_RANGE WHERE USER_ID = :userId",
                 roleQuery="SELECT R.ROLE_ID FROM USER_ROLE UR, ROLE R WHERE UR.USER_ID = :userId AND UR.ROLE_PK = R.ROLE_PK",
                 roleIpRangeQuery="SELECT IP_RANGE FROM ROLE_IP_RANGE WHERE ROLE_ID = :roleId"):
        '''
        Constructor that allows passing custom SQL queries to get the desired info. Override with your custom queries to fit your data model:
        
        userQuery -- SQL query to retrieve list of users. Should return just the user ID column
        userIpRangeQuery -- query to get IP ranges associated with user. Pass in None to disable this functionality
        roleQuery -- query to get list of roles for user. Pass in None to disable this functionality
        roleIpRangeQuery - query to get IP range string column associated with a particular role. Pass in None to disable this functionality 
        '''
        pass
    
##################################################################################################
#
# DECORATORS
#
##################################################################################################    

def secure(roles=None):
    '''
    Main decorator for securing REST endpoints via roles
    '''
    pass
