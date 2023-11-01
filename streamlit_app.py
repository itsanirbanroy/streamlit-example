__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import tempfile
import streamlit as st
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

os.environ["OPENAI_API_KEY"] = "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"

openai_api_key = st.sidebar.text_input('OpenAI API Key')
embeddings_model = None
index = None

st.title("📝 File Q&A ") 
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf")) 

#tmp_location = os.path.join('/tmp', uploaded_file.filename)


#if uploaded_file and not openai_api_key:
    #st.info("Please add your OpenAI API key to continue.")


def createEmbedding():
   if uploaded_file and openai_api_key:
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()

    global index
    embeddings_model = OpenAIEmbeddings()
    index = VectorstoreIndexCreator(embedding=embeddings_model).from_loaders([loader])

def generate_response(input_text):
    global index
    if(index is None):
      createEmbedding()
    #index = VectorstoreIndexCreator(embeddings_model).from_loaders([loader])
    st.info(index.query(input_text))

with st.form('my_form'):
  question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
  )
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(question)