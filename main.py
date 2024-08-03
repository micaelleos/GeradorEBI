
import streamlit as st
import time
from chathandeler import ChatService
from sidebar import sidebar_list
from styles import *

styles()
chat = ChatService()

sidebar_list(chat)

if "chat_id" not in st.session_state:
    st.session_state.chat_id = chat.chat_list()[-1] 

context = "você é um especialista"

if "messages" not in st.session_state:
    st.session_state.messages = chat.history(st.session_state.chat_id)

with st.container():
    
    with st.container():
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            st.title("Assistente de EBI")
        with col2:
            if st.button(":gear:",use_container_width=True):
                pass
    
    col11, col22 = st.columns([0.6,0.4])
    with col11:
        with st.container(border=False):
            chat_container = st.container(height=400,border=False)
            with chat_container:
                initial_message = st.chat_message("assistant")
                initial_message.write("Olá, como posso ajudá-lo hoje?")  
                
                messages = st.session_state.messages

                for i in range(0,len(messages)):
                    message = messages[i]       
                                     
                    if message['role'] == "assistant":
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                    else:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                
            
            prompt = st.chat_input("Faça uma pergunta?",key="user_input")

            if prompt:
                
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                ebi,response=chat.chat(prompt,st.session_state.chat_id,context)
                
                st.session_state.messages.append({"role": "assistant", "content": response})

                st.rerun()

    with col22:
        with st.container(border=True):
            st.write('Estudo biblico')
            #st.write(ebi)