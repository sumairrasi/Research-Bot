
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader
from ResearchBot.agent import ChatModel
from langchain_community.document_loaders import WebBaseLoader
import bs4


class DataIngestion(ChatModel):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def document_loading(self,path):
        loader = PyPDFLoader(file_path=path)
        data = loader.load()
        return data    
    
    def web_loading(self,url):
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    class_=("wrapper__inner","wrapper","post-header")
                )
            )
        )
        data=loader.load()
        return data
    
    def data_store(self,data):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=50)
        texts = text_splitter.split_documents(data)
        embeddings = self.initialize_embeddings()
        PineconeVectorStore.from_documents(texts, embeddings, index_name=self.index_name)
        return True
    
    def data_pipeline(self,data):
        docsearch_data = self.data_store(data)
        return docsearch_data
    
    
