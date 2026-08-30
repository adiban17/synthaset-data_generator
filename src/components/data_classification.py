import sys
from src.exception import CustomException
from src.logger import logging
from src.llm.feature_classification import feature_classification
from typing import List
import streamlit as st
import pandas as pd

class DataClassification:
    def __init__(self, dataset_name: str, features: List[str] ):
        self.dataset_name = dataset_name
        self.features = features

    def data_classification(self):
        try:

            if "classification_started_logged" not in st.session_state:
                logging.info("Feature Classification Started")
                st.session_state.classification_started_logged = True
            

            result = feature_classification(dataset_name=self.dataset_name, features=self.features)
            numerical_features = result.numerical_features
            categorical_features = result.categorical_features

            logging.info(f'Numerical Features: {numerical_features}')
            logging.info(f"Categorical Features: {categorical_features}")

            logging.info("Completed Feature Classification")

        except Exception as e:
            raise CustomException(e, sys)


        try:

            max_length = max(len(numerical_features), len(categorical_features))

            num_padded = numerical_features + ['']*(max_length-len(numerical_features))
            cat_padded = categorical_features + ['']*(max_length - len(categorical_features))

            df = pd.DataFrame({
                'Numerical Features': num_padded,
                'Categorical Features': cat_padded
            })

            st.subheader('Classified Features')
            st.dataframe(df, use_container_width=True, hide_index=True)

            return numerical_features, categorical_features

        except Exception as e:
            raise CustomException(e, sys)