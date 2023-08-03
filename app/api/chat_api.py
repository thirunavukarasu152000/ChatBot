from flask import Blueprint, request
from uuid import uuid4
import os

from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.vectorstores import Weaviate
from langchain.document_loaders import PyPDFium2Loader
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter


from app.prompt import TEMPLATE

chat = Blueprint("Chat-API", __name__, url_prefix="/api")

loader = PyPDFium2Loader("data.pdf")

data = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings()


vectorstore = Weaviate.from_documents(docs, embeddings, weaviate_url=os.environ['WEAVIATE_API_URL'], by_text=False)


MyOpenAI = OpenAI(temperature=0.6)
retriever = vectorstore.as_retriever()

_template = PromptTemplate(
    template=TEMPLATE,
    input_variables=["question", "context", "chat_history"]
)

@chat.route("/question", methods=["POST"])
def question():
    query = request.form["query"]
    conversation_id = request.form["conversation_id"]
    if conversation_id in [None,  '0']:
        conversation_id = uuid4().hex
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    question_answer = ConversationalRetrievalChain.from_llm(MyOpenAI, retriever, memory=memory, 
                                               combine_docs_chain_kwargs={'prompt': _template})
    result = question_answer({"question": query})
    del result["chat_history"]
    return {"ok" : True, "result":result, "conversation_id":conversation_id}
