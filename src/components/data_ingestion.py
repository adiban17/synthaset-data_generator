import sys
from src.exception import CustomException
from src.logger import logging
import streamlit as st
from typing import List

class DataIngestion:
    def __init__(self):
        self.dataset_name = ""
        self.features = []
        self.num_rows = 0

    def ingest_data(self):
        # Input 1: Name of the dataset
        self.dataset_name = st.text_input("Name of the dataset:", placeholder="e.g., Customer Transactions")

        # Input 2: Dynamic Features (Default 2, Max 5)
        if "feature_count" not in st.session_state:
            st.session_state.feature_count = 2


        for i in range(st.session_state.feature_count):
            feat = st.text_input(f"Feature {i + 1}", key=f"feature_{i}")
            self.features.append(feat)

        # Plus button to add more fields (disappears when max 5 is reached)
        if st.session_state.feature_count < 5:
            if st.button("➕ Add Feature"):
                st.session_state.feature_count += 1
                st.rerun()

        # Input 3: Number of rows in the dataset
        self.num_rows = st.number_input("Number of rows:", min_value=1, step=10, value=100)

        st.divider()

        

        # The submit button that triggers the display of the details
        if st.button("Submit"):
            st.write(f"**Dataset Name:** {self.dataset_name}")
            
            # Optional: Filter out empty strings if the user left a feature blank
            valid_features = [f for f in self.features if f.strip()]
            st.write(f"**Features:** {valid_features}")
            
            st.write(f"**Number of Data Points:** {self.num_rows}")

        return self.dataset_name, self.features, self.num_rows

        # --- END NEW UI ---
