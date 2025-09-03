
class AppError(Exception):
    """Erreur générique côté client (400)."""
    status_code = 400


class BadRequestError(AppError):
    status_code = 400


class UnauthorizedError(AppError):
    status_code = 401


class ForbiddenError(AppError):
    status_code = 403


class NotFoundError(AppError):
    status_code = 404
