# Classes des exceptions applicatives customisées

class ApplicationError(Exception):
    """Exception générique pour toutes les erreurs applicatives."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=400)


class UnauthorizedError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=401)


class ForbiddenError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=403)


class NotFoundError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=404)
