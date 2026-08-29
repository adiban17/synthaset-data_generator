import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_agent
from src.utils import clean_output
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate


class FeatureValidationResult(BaseModel):
    is_relevant: bool = Field(
        description="True if all features are relevant to the dataset and output features, False otherwise"
    )
    reasoning: str = Field(
        description="Detailed reasoning explaining why the feature set is relevant or why an irrelevant feature makes it False"
    )


def feature_validation(
    dataset_name: str,
    dataset_features: List[str],
    output_feature: str,
    feature_type: str,
    feature_categories: Optional[List[str]] = None,
)->FeatureValidationResult:
    '''
    Validates whether the provided features and output are relevant to the dataset using LangChain and Pydantic.

    Args:
        dataset_name: Name of the dataset.
        dataset_features: List of input feature names.
        output_feature: Name of the target/output feature.
        feature_type: Type of the output feature ('numerical' or 'categorical').
        feature_categories: List of categories (used only if feature type is categorical).

        Returns:
            FeatureValidationResult contains boolena is_relevant and reasoning.
    '''

    llm = load_agent().with_structured_output(FeatureValidationResult)

    system_prompt = """
    You are an expert machine learning data engineer.
    Your task is to validate whether the given input features and output feature make logical sense and are relevant to the specifier datsset name.
    Analyze if any feature is completely irrelevant, nonsensical, ormismatched for the context of the prediction task.
    Return a boolean feature for is_relevant (True if all features make sense, False if theere is an irrelevant or nonsensical feature) along with clear reasoning.
    """

    human_prompt = """
    Dataset Name: {dataset_name}
    Features: {dataset_features}
    Output Feature: {output_feature}
    Feature Type: {feature_type}
    Output Categories: {feature_categories}

    Validate this configuration.
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt),
        ("human", human_prompt)
        ]
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "dataset_name": dataset_name,
            "dataset_features": dataset_features,
            "output_feature": output_feature,
            "feature_type": feature_type,
            "feature_categories": (
                feature_categories if feature_categories else []
            ),
        }
    )

    return result


# Test
if __name__ == "__main__":
    valid_test = feature_validation(
        dataset_name=" House Price Prediction",
        dataset_features=["area", "number_of_bedrooms", "pincode"],
        output_feature="price",
        feature_type="numerical"
    )

    print("Test 1:")
    print(f"is_relevant:{valid_test.is_relevant}")
    print(f"Reasoning: {valid_test.reasoning}")

    print("\n\n\n")

    invalid_test = feature_validation(
        dataset_name=" Credit Card Fraud Detection",
        dataset_features=["user_id", "cibil_score", "country_of_residence", "penis_size"],
        output_feature="price",
        feature_type="categorical",
        feature_categories=["fraud", "not fraud"]
    )

    print("Test 2:")
    print(f"is_relevant:{invalid_test.is_relevant}")
    print(f"Reasoning: {invalid_test.reasoning}")







