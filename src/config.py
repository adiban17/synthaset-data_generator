import os
import sys
from dotenv import load_dotenv

from langchain.agents import create_agent

from src.logger import logging
from src.exception import CustomException

load_dotenv()

class Config:

    def __init__(self, model_name="claude-sonnet-4-5", system_prompt="You are a helpful assistant"):
        self.llm_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model_name = model_name
        self.system_prompt = system_prompt

    def llm_config(self):
        ANTHROPIC_API_KEY = self.llm_api_key
        MODEL_NAME = self.model_name
        SYSTEM_PROMPT = self.system_prompt

        try:
            if not ANTHROPIC_API_KEY:
                logging.error("Anthropic API Key not found.")
                raise ValueError("Anthropic API Key not found.")
            if not MODEL_NAME:
                logging.error("Model Name not valid.")
                raise ValueError("Model Name not valid.")
            if not SYSTEM_PROMPT:
                logging.error("Invalid System Prompt")
                raise ValueError("Invalid System Prompt")

            agent = create_agent(
                model=MODEL_NAME,
                system_prompt=SYSTEM_PROMPT
            )
            logging.info("Agent Created")

        except Exception as e:
            raise CustomException(e, sys)

        return agent



# Test
if __name__ == "__main__":
    try:
        config = Config(model_name="claude-sonnet-4-6")
        config.llm_config()
    finally:
        logging.info("Test Complete")
        print("Test Complete !")