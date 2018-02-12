class InvalidUsage(Exception):
    """
    An exception indicating a user error.
    """

    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)