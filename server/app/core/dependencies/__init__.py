from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..context import current_user
from ..config.settings import settings
from ..database.database import get_db

from .authentication import *
from .company import *
from .hr import *
from .user import *