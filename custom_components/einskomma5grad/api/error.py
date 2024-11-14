class ApiError(Exception):
    """Base class for all API related errors"""
    pass

class AuthenticationError(ApiError):
    """Raised when there is an authentication error"""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

class TokenError(ApiError):
    """Raised when there is an error retrieving the token"""
    def __init__(self, message="Token retrieval failed"):
        self.message = message
        super().__init__(self.message)

class RequestError(ApiError):
    """Raised when there is an error making a request"""
    def __init__(self, message="Request failed"):
        self.message = message
        super().__init__(self.message)