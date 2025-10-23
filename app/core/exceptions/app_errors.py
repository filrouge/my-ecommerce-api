# Classes des exceptions applicatives customisées

class ApplicationError(Exception):
    """Exception générique pour toutes les erreurs applicatives."""
    status_code: int

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(ApplicationError):
    """ 400 Bad Request """
    status_code: int = 400

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=self.status_code)


class UnauthorizedError(ApplicationError):
    """ 401 Unauthorized """
    status_code: int = 401

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=self.status_code)


class ForbiddenError(ApplicationError):
    """ 403 Forbidden """
    status_code: int = 403

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=self.status_code)


class NotFoundError(ApplicationError):
    """ 404 Not Found """
    status_code: int = 404

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=self.status_code)
