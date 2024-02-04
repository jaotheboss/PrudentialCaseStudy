import os
import openai
import streamlit as st
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.memory import ChatMemoryBuffer
from utils import ContextUtil

# Debugging purposes
debug = eval(os.environ.get("DEBUG", "False"))
if debug:
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Instantiating LLM
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Header for Chat UI
st.header("Chat with PRUmax Plus Training Slides")
if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about PRUmax Plus!"}
    ]

# Load and index data at server instantiation
# cache to prevent multiple loadings of dataset
@st.cache_resource(show_spinner=True)
def load_and_index(path: str = "data") -> VectorStoreIndex:
    """
    Default data path is 'data'. Parses all files in 'path' and indexes them.
    
    Options:
    - SimpleDirectoryReader can be set to 'recursive' for nested files
    - ServiceContext can be passed to 'from_documents' for low-level customization
    """
    
    with st.spinner(text="Loading relevant documents..."):
        try:
            documents = SimpleDirectoryReader(path).load_data()
            index = VectorStoreIndex.from_documents(documents)
            return index
        except openai.AuthenticationError:
            st.error('This solution requires an OpenAI auth key', icon="🚨")
            st.stop()
            
db_index = load_and_index("data")
chat_engine = db_index.as_chat_engine(
    chat_mode="condense_plus_context", 
    memory=ChatMemoryBuffer.from_defaults(token_limit=3900),
    system_prompt=(
        "You are a helpful and joyful financial advisor with the knowledge of a specific insurance product."
        " For any questions relating to this insurance product, you are to provide detailed and accurate information."
        "Your goal is to use the previous chat history, or the context above, to"
        " deliver concise, informative, and user-specific advice or data"
        "For questions outside this product's scope, advise on general insurance guidance or direct the user to appropriate resources."
    ),
    verbose=debug,
    
)


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            print("Validating context")
            response = chat_engine.chat(prompt)
            if ContextUtil.validate_context(response):
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
            else:
                response = "Sorry but your query doesn't seem to be related to information in my database."
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)
