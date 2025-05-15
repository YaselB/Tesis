from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine , select
from domain.message import Message
from domain.base import Base
from infrastructure.user_repository import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_message(id_chat : int , content : str , response : str , type : str):
    session = Session()
    try:
        message = Message(id_chat=id_chat , content= content ,response= response , type= type )
        session.add(message)
        session.commit()
        session.refresh(message)
    except Exception as e:
        session.rollback()
    finally:
        session.close()
def get_message_by_id(id_chat : int):
    session = Session()
    try:
        messages = session.query(Message).filter(Message.id_chat == id_chat).all()
        return messages
    finally:
        session.close()
def get_all_message():
    session = Session()
    try:
        messages = session.execute(select(Message.content)).scalars().all()
        return messages
    finally:
        session.close()