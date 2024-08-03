import streamlit as st

def styles():
    st.markdown("""
                <style>
                div[class="block-container st-emotion-cache-13ln4jf ea3mdgi5"] 
                { 
                max-width: 90vw;
                } 
                
                .st-emotion-cache-12fmjuu{
                height: 1.75rem;
                }

                .st-emotion-cache-13ln4jf{
                padding: 3rem 1rem 10rem;
                }

                .st-emotion-cache-bm2z3a{
                overflow: hidden;
                }

                .st-emotion-cache-4uzi61{
                height: 35vw;
                overflow: auto;
                }
                </style>
                """
                , unsafe_allow_html=True)