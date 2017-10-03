from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from defines import debug
_debug = debug

engine = create_engine('sqlite:///comp1531.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    global _debug
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    #  Delete old tables then re-create - while we work out table format
    if(_debug):
        Base.metadata.drop_all(bind=engine)
    import models
    Base.metadata.create_all(bind=engine)