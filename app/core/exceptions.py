from fastapi import HTTPException, status


class InvalidFileTypeException(HTTPException):
    def __init__(self, detail: str = "Tipo de arquivo inválido"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class FileTooLargeException(HTTPException):
    def __init__(self, detail: str = "Arquivo muito grande"):
        super().__init__(
            status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
            detail=detail
        )


class ConversionException(HTTPException):
    def __init__(self, detail: str = "Erro ao converter arquivo"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
