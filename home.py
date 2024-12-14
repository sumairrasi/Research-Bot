from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from ResearchBot.data_ingestion import DataIngestion
from ResearchBot.agent import ChatModel
import streamlit as st
import tempfile
import os

def app():
    try:
        if 'user' not in st.session_state or not st.session_state.get("logged_in", False):
            st.error("Please log in to access this page.")
            return

        user = st.session_state.user
        role = user.get('role', 'student')
        if role.lower() == 'teacher':
            st.title("Chat with Teacher or Upload Material")
            st.subheader("Upload Teaching Materials")
            uploaded_file = st.file_uploader("Upload a PDF File", type=['pdf'])
            
            if uploaded_file:
                try:
                    temp_dir = tempfile.gettempdir()
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                    
                    data_ingestion = DataIngestion()
                    data = data_ingestion.document_loading(temp_file_path)
                    data_load = data_ingestion.data_pipeline(data)
                    if data_load:
                        with st.spinner("Uploading file to the database..."):
                            st.success("File uploaded to DB successfully!")
                except Exception as e:
                    st.error(f"An error occurred while processing the uploaded file: {e}")
                finally:
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

            st.markdown("#### **Or**")
            url = st.text_input("Enter the URL of the material:")
            if st.button("Submit URL"):
                try:
                    if url:
                        st.info("Processing URL content...")
                        data_ingestion = DataIngestion(
                            groq_api_key=st.secrets['GROQ_API_KEY'],
                            pinecone_api_key=st.secrets["PINECONE_API_KEY"],
                            index_name=st.secrets["PINECONE_INDEX_NAME"]
                        )
                        data = data_ingestion.web_loading(url)  
                        data_load = data_ingestion.data_pipeline(data)
                        if data_load:
                            with st.spinner("Uploading content from URL to the database..."):
                                st.success("URL content uploaded to DB successfully!")
                    else:
                        st.warning("Please enter a valid URL.")
                except Exception as e:
                    st.error(f"An error occurred while processing the URL: {e}")
        else:
            st.subheader("Chat with Teacher")
            if 'messages' not in st.session_state:
                st.session_state['messages'] = [{"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}]

            with st.container():
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for msg in st.session_state.messages:
                    avatar = "👩‍🎤" if msg["role"] == "assistant" else "👩‍🎓"
                    with st.chat_message(msg["role"], avatar=avatar):
                        st.write(msg["content"])
                st.markdown('</div>', unsafe_allow_html=True)

            prompt = st.chat_input("Say something")
            if prompt:
                try:
                    if "agent_executer" not in st.session_state:
                        st.session_state.agent_executer = ChatModel(
                            groq_api_key=st.secrets['GROQ_API_KEY'],
                            pinecone_api_key=st.secrets["PINECONE_API_KEY"],
                            index_name=st.secrets["PINECONE_INDEX_NAME"]
                        ).chat_main()

                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.chat_message("user", avatar="👩‍🎓").write(prompt)

                    with st.chat_message("bot", avatar="👩‍🎤"):
                        st_callback = StreamlitCallbackHandler(st.container())
                        response = st.session_state.agent_executer.invoke(
                            {"input": prompt, "chat_history": st.session_state.messages}, {"callbacks": [st_callback]}
                        )
                        st.session_state.messages.append({"role": "assistant", "content": response["output"]})
                        st.write(response["output"])
                except Exception as e:
                    st.error(f"An error occurred while processing your input: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")