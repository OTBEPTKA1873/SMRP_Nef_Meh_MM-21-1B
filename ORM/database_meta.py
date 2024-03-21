from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///./DataBase_dbeaver")
get_session = sessionmaker(engine, autocommit=False)
