from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.context import current_user
from app.core.config.settings import settings
from app.core.database.database import get_db

from app.core.dependencies.authentication import *
from app.core.dependencies.company import *
from app.core.dependencies.hr import *
from app.core.dependencies.user import *
from app.core.dependencies.utilities import *
