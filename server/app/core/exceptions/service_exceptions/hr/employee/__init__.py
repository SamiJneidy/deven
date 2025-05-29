from app.core.exceptions.service_exceptions.hr.employee.employee import (
    EmployeeNotFoundException,
    WorkEmailAlreadyInUseException,
    PersonalEmailAlreadyInUseException,
)
from app.core.exceptions.service_exceptions.hr.employee.document import (
    EmployeeDocumentUploadFailedException,
    EmployeeDocumentNotFoundException,
)
from app.core.exceptions.service_exceptions.hr.employee.education import EmployeeEducationNotFoundException