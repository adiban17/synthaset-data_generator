import sys
import streamlit as st
from src.logger import logging
from src.exception import CustomException
from src.config import Config

def clean_output(ai_response)->str:
    '''
    ai_response: raw AI Message 
    Converts AI Message to clean readable content
    '''
    try:
        clean_response = ai_response.content
        return clean_response
    except Exception as e:
        logging.info(e)
        raise CustomException(e, sys)


@st.cache_resource
def load_agent():
    try:
        config = Config()
        return config.llm_config()
    except Exception as e:
        raise CustomException(e, sys)

# Test
if __name__=="__main__":
    try:
        llm = load_agent()
        result=llm.invoke("What is the captial of Maharashtra ?")
        print(clean_output(result))
    except Exception as e:
        raise CustomException(e, sys)