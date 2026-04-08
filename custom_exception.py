class EbutouyExceptions(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"Error: {self.message}\nError Code: {self.error_code}"

class InputError(EbutouyExceptions):
    def __init__(self):
        super().__init__("Invalid URL", 100)

class DownloadError(EbutouyExceptions):
    def __init__(self):
        super().__init__("Can't Download Video", 110)

class NilStreams(EbutouyExceptions):
    def __init__(self):
        super().__init__("No Streams For The Video", 120)

class UpdateError(EbutouyExceptions):
    def __init__(self):
        super().__init__("Update your app", 190)

class NukedError(EbutouyExceptions):
    def __init__(self):
        super().__init__("The app isnt working properly check for updates", 200)