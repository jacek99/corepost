'''
Common classes
'''

class Response:
    """
    Custom response object, can be returned instead of raw string response
    """
    def __init__(self,code=200,entity=None,headers={}):
        self.code = code
        self.entity=entity
        self.headers=headers  
        
    def __str__(self):
        return str(self.__dict__)