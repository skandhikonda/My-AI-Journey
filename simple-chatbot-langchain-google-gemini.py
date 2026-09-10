# creating a simple chatbot using langchain and google gemini

import os # module
from langchain_google_genai import ChatGoogleGenerativeAI # class

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") # function
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=GOOGLE_API_KEY) # class

question = input("What is your question? ") # function
response = llm.invoke(question) # method
print(response.content[0]["text"]) # function
