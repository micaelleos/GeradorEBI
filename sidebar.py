import streamlit as st
import uuid
from chathandeler import ChatService

def novo_chat():
    chat_id = str(uuid.uuid1())
    st.session_state.chat_id = chat_id
    st.session_state.messages = []
    

def sidebar_list(chat):
    list = chat.chat_list()
    with st.sidebar:
        if st.button("Novo chat",use_container_width=True):
            novo_chat()
        with st.container(border=True, height=300):
            for item in list:
                if st.button('Chat '+item['SessionId'],use_container_width=True):
                    st.session_state.chat_id = item['SessionId']
                    st.session_state.messages = chat.history(st.session_state.chat_id)
                    