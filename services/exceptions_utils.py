
class BadRequestError(Exception):
    """Erreur générique côté client (400)."""
    status_code = 400


class UnauthorizedError(BadRequestError):
    status_code = 401


class ForbiddenError(BadRequestError):
    status_code = 403


class NotFoundError(BadRequestError):
    status_code = 404
