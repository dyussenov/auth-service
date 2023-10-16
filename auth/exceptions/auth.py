class AuthException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __repr__(self):
        return self.message
