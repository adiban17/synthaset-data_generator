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
        clean_response = ai_response['messages'][-1].content
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