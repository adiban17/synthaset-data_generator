import sys
from src.exception import CustomException
from src.logger import logging
from typing import List, Optional
import streamlit as st
from src.llm.feature_validation import feature_validation # Assuming feature_validation.py is inside src/llm/

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
        # Fixed typo, removed num_rows, and used keyword arguments
        result = feature_validation(
            dataset_name=self.dataset_name,
            dataset_features=self.features,
            output_feature=self.output_feature,
            feature_type=self.output_type,
            feature_categories=self.feature_categories
        )
        is_relevant = result.is_relevant
        reasoning = result.reasoning

        st.divider() # Adds a clean horizontal line
        st.subheader("Validation Results")

        # Display a colored alert based on whether the validation passed or failed
        if is_relevant:
            st.success("✅ Validation Passed: All features are relevant.", icon="✅")
        else:
            st.error("❌ Validation Failed: Irrelevant or mismatched features detected.", icon="🚨")

        # Put the verbose reasoning inside a clean container
        with st.expander("View Detailed Reasoning", expanded=True):
            st.markdown(f"**Agent Reasoning:**\n\n{reasoning}")

        