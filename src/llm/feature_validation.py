import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_agent
from src.utils import clean_output
from typing import List

def feature_validation(dataset_name:str, features:List)->bool:
    '''
    this function performs feature validation on the input data
    '''
    agent = load_agent()
    result = agent.invoke({"messages": [("user", "What is the capital of India ?")]})
    print(clean_output(result))


# Test
if __name__ == "__main__":
    feature_validation(dataset_name="", features=[])



