from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from domain.user import User
from domain.base import Base


DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/tesis"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_user(name: str, email: str = None):
    session = Session()
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
def get_user_by_email(email: str):
    session = Session()
    try:
        user = session.query(User).filter(User.email == email).first()
        return user
    finally:
        session.close()
def get_user_by_Id(id_user: int):
    session = Session()
    try:
        user = session.query(User).filter(User.id_user == id_user).first()
        return user
    finally:
        session.close()