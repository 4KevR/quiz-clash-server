import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg://{os.environ['POSTGRES_USER']}:" \
                          f"{os.environ['POSTGRES_PASSWORD']}" \
                          f"@db:5432/{os.environ['POSTGRES_DB']}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
