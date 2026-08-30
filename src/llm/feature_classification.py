import sys
from unittest import result
from src.exception import CustomException
from src.logger import logging
from pydantic import BaseModel, Field
from src.utils import load_agent
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Optional

# Pydantic Structured Output
class FeatureClassificationResult(BaseModel):
    numerical_features: List[str] = Field(
        description="Numerical Features from the list of features."
    )
    categorical_features: List[str] = Field(
        description="Features that are of object type."
    )


def feature_classification(dataset_name: str, features: List[str])->FeatureClassificationResult:
    '''
    Categorizes the features into numerical and categorical using Pydantic and Langchain

    Args:
        features: List of features that need to be categorized.

        Returns:
            FeatureClassificationResult which contains numerical_features and categorical_features
    '''

    try:

        llm = load_agent().with_structured_output(FeatureClassificationResult)

        system_prompt = """
        You are an expert machine learning data engineer.
        Your task is to categorize the given input features are numerical_features or categorical_features in context to the dataset name provided. 
        Return a list of numerical features and a list of categorical features.
        """


        human_prompt = """
        Dataset Name: {dataset_name}
        Features: {features}

        Classify these features into numerical and categorical features in context to the dataset name provided.
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", human_prompt)
            ]
        )

        chain = prompt | llm

        result = chain.invoke(
            {
                "dataset_name": dataset_name,
                "features": features
            }
        )

        return result




    except Exception as e:
        raise CustomException(e, sys)




# Test
if __name__ == "__main__":
    try:
        dataset_name = "House Price Prediction"
        features = ['area', 'name', 'number_of_bedrooms', 'pincode']
        result = feature_classification(dataset_name=dataset_name, features=features)
        print(f"Categorical Features: {result.categorical_features}")
        print(f"Numerical Features: {result.numerical_features}")
    except Exception as e:
        raise CustomException(e, sys)


