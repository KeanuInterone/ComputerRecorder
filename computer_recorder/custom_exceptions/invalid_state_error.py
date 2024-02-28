

class InvalidStateError(Exception):
    """Exception raised when an object is in an invalid state."""
    def __init__(self, message="Invalid state"):
        self.message = message
        super().__init__(self.message)