import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup

load_dotenv()
# Setting page title and header
st.set_page_config(page_title="URL Summarizer ", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>URL Summarizer </h1>", unsafe_allow_html=True)

st.session_state['URL']=st.text_input("Past  URL Here ",type="default")
summarise_button = st.button("Summarise the URL", key="summarise")

# Send a GET request to the URL
url = "https://vkaps.com/"
if st.session_state['URL'] !="":
  url = st.session_state['URL']
response = requests.get(url,verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')

    with open('scraped_data.txt', 'w', encoding='utf-8') as file:
        # Iterate over the found elements and write their text content to the file
        for paragraph in paragraphs:
            file.write(paragraph.get_text(strip=True) + '\n')


# Open the text file in read mode
with open('scraped_data.txt', 'r') as file:
    # Read the entire contents of the file into a string
    data = file.read()
#  prompt_template
prompt_template = PromptTemplate.from_template(
    """write the summary of {data}   about {no} words for{app} post
    Please provide a concise summary of the provided information."""
)
prompt=prompt_template.format(data=data,no=500, app="samerizer app")
llm=OpenAI()
dataa=(llm(prompt=prompt))
if 'messages' not in st.session_state:
    st.session_state['messages'] =[]
# #####
if summarise_button:
    if st.session_state['URL'] =="":
        st.error("Please Enter The Website Url")
    else:
        summarise_placeholder = st.write(dataa)
