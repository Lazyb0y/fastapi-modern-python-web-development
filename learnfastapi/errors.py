class DuplicateError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class MissingError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
