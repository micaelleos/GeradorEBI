
import streamlit as st
import time
from chathandeler import ChatService
from sidebar import sidebar_list
from styles import *

def atualizar_estudo(ebi):
    print(ebi)
    if ebi:
        st.session_state.title = ebi["title"]
        st.session_state.base = ebi["base"]
        st.session_state.description = ebi["description"]
        st.session_state.footer = ebi["footer"]

if "title" not in st.session_state: 
    st.session_state.title = ""
    st.session_state.base = ""
    st.session_state.description = ""
    st.session_state.footer = ""
    


styles()
chat = ChatService()

sidebar_list(chat)

if "chat_id" not in st.session_state:
    st.session_state.chat_id = chat.chat_list()[-1] 

context = "você é um especialista"

if "messages" not in st.session_state:
    st.session_state.messages = chat.history(st.session_state.chat_id)

with st.container():
    col11, col22 = st.columns([0.6,0.4])
    with col11:
        with st.container():
            with st.container():
                col1, col2 = st.columns([0.8,0.2])
                with col1:
                    st.title("Assistente de EBI")
                with col2:
                    if st.button(":gear:",use_container_width=True):
                        pass

            for message in st.session_state.messages:
                if message['role'] == "assistant":
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                else:
                    with st.chat_message(message["role"]): 
                        st.markdown(message["content"])
                

            if prompt := st.chat_input("Faça uma pergunta?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner(''):
                        ebi,response=chat.chat(prompt,st.session_state.chat_id,context)
                        atualizar_estudo(ebi)
                    st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    with col22:
        with st.container(border=True,height=1000):
            st.write(st.session_state.title)
            st.write(st.session_state.base)
            st.write(st.session_state.description)
            st.write(st.session_state.footer)