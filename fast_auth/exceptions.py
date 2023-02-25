class FastAuthAppError(Exception):
    pass


class BadRequestError(FastAuthAppError):
    pass


class EntityNotFoundError(FastAuthAppError):
    pass


class DuplicateEntityError(FastAuthAppError):
    pass


class DuplicateUserError(DuplicateEntityError):
    pass


class UnauthorizeError(FastAuthAppError):
    pass
