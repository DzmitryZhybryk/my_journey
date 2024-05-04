class NoGeographicDataException(Exception):

    def __init__(self, message: str) -> None:
        self.message = message


class ExternalServiceError(Exception):
    pass
