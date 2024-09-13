import os
from typing import List, Literal
from pydantic import BaseModel, Field
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.prompts import MessagesPlaceholder
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate

from langchain.memory import ConversationBufferMemory

from src.tool import generate_tools_for_user

@st.cache_resource()
def memory():
    memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
    return memory

class EBIagent:
    def __init__(self):

        self.OPENAI_API_KEY=os.environ['OPENAI_API_KEY'] #pegar do .env

        self.model = ChatOpenAI(openai_api_key=self.OPENAI_API_KEY,temperature=0.5, model="gpt-4o")

        self.exibir_ebi = generate_tools_for_user()

        self.model_with_tool = self.model.bind(functions=[convert_to_openai_function(self.exibir_ebi)])

        self.memory=memory()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """ Você é um especialista em teologia e em criação de estudo bíblico indutivo.
            Sua base bíblica é batista
            O estudo bíblico deve ser bem completo, com texto de referência, e com no mínimo 10 perguntas (Observação, interpretação e aplicação)
            Você cria estudo bíblicos voltados para jovens
            Você deve auxilixar o usuário a construir um EBI com base num texto bíblico
            Você deve sempre exibir o estudo bíblico, por meio da ferramenta "exibir_ebi"
            você deve colocar o trecho do texto base no EBI 
            Caso o usuário solicite mudandas no EBI você deve executá-la e sempre exibir o estudo bíblico com a modificação
            Você não pode repedir ao usuário o EBI, apenas exiba por meio da ferramenta "exibir_ebi"
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent_chain = RunnablePassthrough.assign(
            agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | self.prompt | self.model_with_tool | OpenAIFunctionsAgentOutputParser()

        self.agent_executor = AgentExecutor(agent=self.agent_chain, tools=[self.exibir_ebi], verbose=True, memory=self.memory,handle_parsing_errors=True)

    def chat_agent(self,query):    
        response=self.agent_executor.invoke({'input':query})
        return response
    