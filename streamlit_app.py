import streamlit as st
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai_api_key = st.sidebar.text_input('OpenAI API Key')

st.title("📝 File Q&A ") 
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md")) 


if uploaded_file and question and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if uploaded_file and question and openai_api_key:
    loader = PyPDFLoader(uploaded_file)
    pages = loader.load_and_split()
    embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

def generate_response(input_text):
    index = VectorstoreIndexCreator(embeddings_model).from_loaders([loader])
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