# coding=utf-8


class GateguardError(Exception):

    pass


class ValidationError(GateguardError):

    def __init__(self, error=None, code=None):
        self.error = error
        self.code = code

        super().__init__(self.error)
