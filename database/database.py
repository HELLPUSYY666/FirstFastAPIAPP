from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg2://zakariyapolevchishikov:12345@localhost:5432/fast_api_db')

Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session

