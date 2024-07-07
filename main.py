
import streamlit as st
import time
from chathandeler import ChatService
from sidebar import sidebar_list

chat = ChatService()

sidebar_list(chat)

if "chat_id" not in st.session_state:
    st.session_state.chat_id = chat.chat_list()[-1] 

context = "você é um especialista"

if "messages" not in st.session_state:
    st.session_state.messages = chat.history(st.session_state.chat_id)

with st.container():
    col1, col2 = st.columns([0.8,0.2])
    with col1:
        st.title("Agente Funcional")
    with col2:
        if st.button(":gear:",use_container_width=True):
            pass


initial_message = st.chat_message("assistant")
initial_message.write("Olá, como posso ajudá-lo hoje?")  

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
            response=chat.chat(prompt,st.session_state.chat_id,context)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
