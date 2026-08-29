import sys
from src.exception import CustomException
from src.logger import logging
from typing import List, Optional
import streamlit as st
from src.llm.feature_validation import feature_validation 

class DataValidation:
    def __init__(
        self,
        dataset_name:str,
        features:List[str],
        num_rows: int,
        output_feature: str,
        output_type: str,
        feature_categories: Optional[List[str]] 
        ):
        self.dataset_name = dataset_name
        self.features = features
        self.num_rows = num_rows
        self.output_feature = output_feature
        self.output_type = output_type
        self.feature_categories = (
                feature_categories if feature_categories else []
            )

    def data_validation(self):
        
        try:
            logging.info("Data Validation Started.")
            result = feature_validation(
                dataset_name=self.dataset_name,
                dataset_features=self.features,
                output_feature=self.output_feature,
                feature_type=self.output_type,
                feature_categories=self.feature_categories
            )

            is_relevant = result.is_relevant
            reasoning = result.reasoning

            st.divider() 


            # Display results
            st.subheader("Validation Results")
            
            if is_relevant:
                st.success(" Validation Passed: All features are relevant.")
            else:
                st.error("Validation Failed: Irrelevant or mismatched features detected.")

            
            with st.expander("View Detailed Reasoning", expanded=True):
                st.markdown(f"**Agent Reasoning:**\n\n{reasoning}")

            # Logs
            logging.info(f"is_relevant: {is_relevant}")
            logging.info(f"Reasoning: {reasoning}")
            logging.info("Data Validation Complete !")

        except Exception as e:
            raise CustomException(e, sys)
        