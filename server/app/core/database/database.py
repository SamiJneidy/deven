from sqlalchemy import and_, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from app.core.context import current_company
from app.core.config.settings import settings

# DB_URL = f"postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"
engine = create_engine(settings.SQLALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@event.listens_for(Session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    if (
        execute_state.is_select and
        not execute_state.is_column_load and
        not execute_state.is_relationship_load and
        not execute_state.execution_options.get("skip_global_filters", False)
    ):
        stmt = execute_state.statement
        froms = []
        
        try:
            froms = stmt.get_final_froms() or []
        except AttributeError:
            pass
            
        filters = []
        
        try:
            company_id = current_company.get().id
        except:
            return
        
        for from_clause in froms:
            # Handle Core Table objects and aliases
            if hasattr(from_clause, 'c'):
                if 'company_id' in from_clause.c:
                    filters.append(from_clause.c.company_id == company_id)
                # Handle table aliases
                elif hasattr(from_clause, 'original') and 'company_id' in from_clause.original.c:
                    filters.append(from_clause.original.c.company_id == company_id)
            
            # Handle ORM mappers
            elif hasattr(from_clause, 'entity_namespace'):
                mapper = from_clause.entity_namespace
                if hasattr(mapper.class_, 'company_id'):
                    filters.append(mapper.class_.company_id == company_id)
        
        if filters:
            if len(filters) == 1:
                execute_state.statement = stmt.where(filters[0])
            else:
                execute_state.statement = stmt.where(and_(*filters))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
