
class EbutouyExceptions(Exception):
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        return f"Error: {self.message}\nError Code: {self.error_code}"


class InvalidURLError(EbutouyExceptions):
    def __init__(self, details: str = ""):
        message = f"Invalid URL{f': {details}' if details else ''}"
        super().__init__(message, 100)


class DownloadFailedError(EbutouyExceptions):
    def __init__(self, details: str = ""):
        message = f"Can't Download Video{f': {details}' if details else ''}"
        super().__init__(message, 110)


class NoStreamsError(EbutouyExceptions):
    def __init__(self, details: str = ""):
        message = f"No Streams For The Video{f': {details}' if details else ''}"
        super().__init__(message, 120)


class MetadataError(EbutouyExceptions):
    def __init__(self, details: str = ""):
        message = f"Metadata Operation Failed{f': {details}' if details else ''}"
        super().__init__(message, 130)


class FileOperationError(EbutouyExceptions):
    def __init__(self, details: str = ""):
        message = f"File Operation Failed{f': {details}' if details else ''}"
        super().__init__(message, 140)
