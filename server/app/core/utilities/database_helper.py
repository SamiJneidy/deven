from app.core.exceptions import ForeignKeyViolationException, UniqueConstraintViolationException, IntegrityException

def raise_classified_integrity_error(e: Exception) -> Exception:
    """Classifies the integrity error into UNIQUE CONSTRAINT or FK CONSTRAINT and raises the appropriate exception.
    Note, it raises a general IntegrityException in case of failure to classify the exception."""
    error_message = str(e.orig).lower()
    print(error_message)
    if "foreign key" in error_message:
        raise ForeignKeyViolationException()
    elif "unique" in error_message:
        raise UniqueConstraintViolationException()
    else:
        raise IntegrityException()
