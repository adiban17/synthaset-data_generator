import sys
from src.exception import CustomException
from src.logger import logging
from src.config import Config
from src.utils import clean_output
import streamlit as st


st.title("SynthSet POC")

@st.cache_resource
def load_agent():
    try:
        config = Config()
        return config.llm_config()
    except Exception as e:
        raise CustomException(e, sys)

agent = load_agent()
logging.info("Agent Loaded")

user_query = st.text_input("Ask:", placeholder="e.g., What is the full form of BBC?")
logging.info(f"User Query:{user_query}")

try:
    if st.button("Shoot"):
        if user_query:
            with st.spinner("Thinking..."):
                result = agent.invoke({"messages": [("user", user_query)]})
                answer = clean_output(result)
                logging.info(f"Response:{answer}")
                st.write("**Response:**")
                st.info(answer)
        else:
            st.warning("Please enter a question first.")
except Exception as e:
    raise CustomException(e, sys)