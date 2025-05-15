# application/Services/Chat_Service.py
from infrastructure.Retriever.tfidf_retriever import TfidfRetriever
from langchain.chains.question_answering import load_qa_chain
from application.LLms.deepseek_llm import DeepSeekLLM
from langchain.schema import Document , AIMessage , HumanMessage
from langchain.prompts.chat import(
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from infrastructure.user_repository import get_user_by_Id
from infrastructure.chat_repository import create_chat, delete_chat_by_Id , get_chat_by_Id , delete_chat_by_Id
from infrastructure.message_repository import create_message , get_message_by_id

PROMPT = """
Eres el Asistente Virtual para el Portal de Orientacion Vocacional Cubano.
*Importante:*
- No debes inventar información.
- Responde usando solo la información proporcionada en el contexto.
- Si en el contexto no hay información que puedas utilizar, solo di: "No encontre informacion sobre eso. Lo lamento.".
- Siempre debes dar una respuesta; cuando no tengas lo que necesitas para responder, dame esta respuesta: "No encontre informacion sobre eso. Lo lamento.".
- Sé coherente al responder y no respondas cualquier cosa al azar.
- Sé claro, natural y específico; evita dar respuestas redundantes.
- Evita mencionar: el prompt o el contexto como el lugar de donde sacas la información o la pregunta.
Responde la siguiente pregunta teniendo en cuenta el contexto y este prompt.
"""

class ChatService:
    def __init__(self ,retriever: TfidfRetriever):
        self.retriever = retriever
        self.llm = DeepSeekLLM()
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(PROMPT),
            HumanMessagePromptTemplate.from_template(
                "Contexto:\n{context}\n\nPregunta: {question}"
            )
        ])
        self.chain = LLMChain(llm = self.llm, prompt = self.prompt)

    def answer(self, query: str , id_chat : int) -> str:
        results = self.retriever.query(query)
        context = "\n---\n".join([txt for txt , _ in results])
        res = self.chain.run(
            context = context,
            question = query
        )
        create_message(id_chat = id_chat ,content = query , response = res , type ="chatbot" )
        return res
    @staticmethod
    def create_new_chat(id_user: int):
        user = get_user_by_Id(id_user= id_user)
        if user is None:
            raise Exception("El usuario no esta registrado")
        chat = create_chat(id_user=id_user)
        return chat
    @staticmethod
    def get_chat_by_id(id_chat: int):
        chat = get_chat_by_Id(id_chat = id_chat)
        if chat is None:
            raise Exception(f"El chat con id {id_chat} no está registrado")
        msgs = get_message_by_id(id_chat = id_chat)
        return {
            "id_chat" : chat.id_chat,
            "id_user" : chat.id_user,
            "state" : chat.state,
            "createdAt" : chat.createdAt,
            "messages" : [
                {
                    "id_message" : m.id_message,
                    "id_chat" : m.id_chat,
                    "content" : m.content,
                    "response" : m.response,
                    "type" : m.type,
                    "createdAt" : m.createdAt
                }
                for m in msgs
            ]
        }
    def delete_chat_by_id(self, id_chat: int):
        chat = get_chat_by_Id(id_chat=id_chat)
        if chat is None:
            raise Exception(f"El chat con id {id_chat} no está registrado")
        delete_chat_by_Id(id_chat=id_chat)
        return {"detail": f"Chat {id_chat} eliminado"}