class NashApiRequestException(Exception):
    
    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message
