import streamlit as st

def sidebar_list(chat):
    list = chat.chat_list()
    with st.sidebar:
        with st.container(border=True, height=300):
            for item in list:
                if st.button('Chat '+item['SessionId'],use_container_width=True):
                    st.session_state.chat_id = item['SessionId']
                    st.session_state.messages = chat.history(st.session_state.chat_id)
                    