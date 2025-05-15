from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete
from domain.chat import Chat
from domain.base import Base
from domain.message import Message
from infrastructure.user_repository import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
def create_chat(id_user: int):
    session = Session()
    try:
        chat = Chat(id_user=id_user)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
def get_chat_by_Id(id_chat: int):
    session = Session()
    try:
        chat = session.query(Chat).filter(Chat.id_chat == id_chat).first()
        return chat
    finally:
        session.close()
def delete_chat_by_Id(id_chat: int):
    session = Session()
    try:
        session.query(Message).filter(Message.id_chat == id_chat).delete()
        session.query(Chat).filter(Chat.id_chat == id_chat).delete()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
