class QuantumCoreException(Exception):
    """common base class for all exceptions in QuantumCore"""
    
class NotFound(QuantumCoreException):
    """a resource could not be found"""
    
    def __init__(self, url, msg=u''):
        self.msg = msg
        self.url = url
        
    def __str__(self):
        return "Resource '%s' could not be found: %s" %(self.url, self.msg)