from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import re

hostIP = 'http://192.168.178.89:11434'

def _combine_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

def _getFormattedContext(menu_str, question):
    splitOnDays = menu_str.split("##")[1:]
    #days_list = [re.search(r'This is list of what is available on (\w+):', item).group(1) for item in splitOnDays]
    daysList = []
    for item in splitOnDays:
          daysList.append(re.search(r'Menu for (\w+):', item).group(1))
    # Needs to be done through Ollama, due to formatting
    mistralEmbeddings = OllamaEmbeddings(model="mistral-nemo",base_url=hostIP)


    #create a vectorstore for each day of the week
    vectorstore = Chroma.from_texts(texts=splitOnDays, embedding=mistralEmbeddings,ids=daysList)


    # Retrieve the context for the question
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.invoke(question)
    formatted_context = _combine_docs(retrieved_docs)
    return formatted_context

def getFormattedContext(menu_str,question):
      formattedContext =  _getFormattedContext(menu_str,question)
      #print(formattedContext)
      return formattedContext