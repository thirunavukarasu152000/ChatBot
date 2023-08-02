from dotenv import load_dotenv
load_dotenv()

import os
import json

from langchain.document_loaders import PyPDFium2Loader
from langchain.llms import OpenAI
from langchain.document_loaders import PDFMinerLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Weaviate
from langchain import PromptTemplate,LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import weaviate


loader = PyPDFium2Loader("data.pdf")

data = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings()

vectorstore = Weaviate.from_documents(docs, embeddings, weaviate_url=os.environ['WEAVIATE_API_URL'], by_text=False)


auth_config = weaviate.AuthApiKey(api_key=os.environ['WEAVIATE_API_KEY'])
client = weaviate.Client(url=os.environ['WEAVIATE_API_URL'], auth_client_secret=auth_config)

schema = client.schema.get()

print(json.dumps(schema, indent=4))
