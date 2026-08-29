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
        self.output_feature = ""
        self.feature_type = ""
        self.output_categories = []

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

        # --- NEW INPUTS: Output Feature and Feature Type ---
        self.output_feature = st.text_input("Output Feature Name:", placeholder="e.g., Churn Status")
        
        self.feature_type = st.selectbox("Feature Type:", options=["Numerical", "Categorical"])

        # Dynamic Categories if Categorical is selected
        if self.feature_type == "Categorical":
            if "category_count" not in st.session_state:
                st.session_state.category_count = 2

            for i in range(st.session_state.category_count):
                cat = st.text_input(f"Category {i + 1}", key=f"category_{i}")
                self.output_categories.append(cat)

            if st.session_state.category_count < 5:
                if st.button("➕ Add Category"):
                    st.session_state.category_count += 1
                    st.rerun()
                    
        st.divider()

        # The submit button that triggers the display of the details
        if st.button("Submit"):
            st.write(f"**Dataset Name:** {self.dataset_name}")
            
            # Optional: Filter out empty strings if the user left a feature blank
            valid_features = [f for f in self.features if f.strip()]
            st.write(f"**Features:** {valid_features}")
            
            st.write(f"**Number of Data Points:** {self.num_rows}")
            
            # Display new inputs
            st.write(f"**Output Feature:** {self.output_feature}")
            st.write(f"**Feature Type:** {self.feature_type}")
            
            if self.feature_type == "Categorical":
                valid_categories = [c for c in self.output_categories if c.strip()]
                st.write(f"**Output Categories:** {valid_categories}")

        return self.dataset_name, self.features, self.num_rows, self.output_feature, self.feature_type, self.output_categories
