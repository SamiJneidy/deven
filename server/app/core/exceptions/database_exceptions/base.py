class UniqueConstraintViolationException(Exception):
    def __init__(self, detail: str = "Unique constraint violation. Duplicate entry found."):
        self.detail = detail

class ForeignKeyViolationException(Exception):
    def __init__(self, detail: str = "Foreign key constraint violation. Related record not found."):
        self.detail = detail

class IntegrityException(Exception):
    def __init__(self, detail: str = "An integrity error has occurred."):
        self.detail = detail
