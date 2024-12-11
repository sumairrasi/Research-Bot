from ResearchBot.config import VectorDBConfigurations
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.agents import create_openai_tools_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from dotenv import load_dotenv
load_dotenv()




class ChatModel:
    def __init__(self,groq_api_key,pinecone_api_key,index_name):
        self.groq_api_key = groq_api_key
        self.pinecone_api_key = pinecone_api_key
        self.index_name = index_name
    
    def initialize_llm(self):
        llm = ChatGroq(groq_api_key=self.groq_api_key,model="Llama3-8b-8192")
        return llm

    def initialize_embeddings(self):
        embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
        return embeddings
    
    def initialize_tools(self):
        api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
        wiki_tool=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
        api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
        arxiv_tool=ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
        return wiki_tool, arxiv_tool
    
    def initialize_vectordb(self,index_name, embeddings):
        VectorDBConfigurations(self.pinecone_api_key,index_name)
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        retriever_tool = create_retriever_tool(retriever, "AI-learning", "Search and return information")
        return retriever_tool
    
    def create_prompt_template(self):
        return ChatPromptTemplate.from_messages([
            (
                "You are a professional teacher for answering questions. "
                "You have access to the following tools. Use the retrieved context to answer "
                "the question. If you don't know the answer, say so. Use three sentences "
                "maximum and keep the answer concise.\n\n"
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    def initialize_agent(self,llm,tools,prompt_template):
        agent = create_openai_tools_agent(llm, tools, prompt_template)
        agent_executer = AgentExecutor(agent=agent,tools=tools,verbose=True)
        return agent_executer  
    
    def chat_main(self):
        llm = self.initialize_llm()
        embedding = self.initialize_embeddings()
        additional_tools = self.initialize_tools()
        vectorestore = self.initialize_vectordb(self.index_name,embedding)
        chat_prompt= self.create_prompt_template()
        tools = [vectorestore,*additional_tools]
        agent = self.initialize_agent(llm, tools, chat_prompt)
        return agent
        
        


    