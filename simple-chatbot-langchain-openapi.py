# creating a simple chatbot using langchain and openai api

import os # module
from langchain_openai import ChatOpenAI

OPEN_API_KEY = os.environ.get("OPENAI_API_KEY") # function
llm = ChatOpenAI(model="gpt-4o", api_key=OPEN_API_KEY) # class

question = input("What is your question? ") # function
response = llm.invoke(question) # method
print(response.content) # function
