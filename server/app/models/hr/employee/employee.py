from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey, Boolean, Enum as SQLEnum, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.enums import EmployeeStatus, Gender, MartialStatus
from app.models.common import AddressMixin, BaseModel

class Employee(Base, BaseModel, AddressMixin):
    __tablename__ = "employees"
    # Personal info
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    martial_status = Column(SQLEnum(MartialStatus), nullable=True)
    children = Column(Integer, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    profile_picture_public_id = Column(String, nullable=True)
    # Contact
    work_email = Column(String, nullable=False, unique=True)
    personal_email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True, unique=True)
    emergency_phone = Column(String, nullable=True)
    emergency_email = Column(String, nullable=True)
    # Job info
    job_title_id = Column(Integer, ForeignKey('job_titles.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    shift_id = Column(Integer, ForeignKey('shifts.id'), nullable=True)
    work_type_id = Column(Integer, ForeignKey('work_types.id'), nullable=False)
    reporting_manager_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    date_of_joining = Column(DateTime, nullable=False)
    in_probation = Column(Boolean, nullable=False)
    probation_period = Column(Integer, nullable=True)
    # System info
    status = Column(SQLEnum(EmployeeStatus), nullable=False)

    job_title = relationship("JobTitle", foreign_keys=[job_title_id], back_populates="employees")
    department = relationship("Department", foreign_keys=[department_id], remote_side="Department.id", back_populates="employees")
    shift = relationship("Shift", foreign_keys=[shift_id])
    work_type = relationship("WorkType", foreign_keys=[work_type_id], back_populates="employees")
    reporting_manager = relationship("Employee", foreign_keys=[reporting_manager_id], remote_side=[id], back_populates="subordinates")
    subordinates = relationship("Employee", foreign_keys=[reporting_manager_id], back_populates="reporting_manager")
    location = relationship("Location", foreign_keys=[location_id], back_populates="employees")
    education = relationship("EmployeeEducation", back_populates="employee")
    documents = relationship("EmployeeDocument", back_populates="employee")
    company = relationship("Company", back_populates="employees")
