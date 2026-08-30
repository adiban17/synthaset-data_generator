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

        try:

            if "ingestion_started_logged" not in st.session_state:
                logging.info("Started Data Ingestion")
                st.session_state.ingestion_started_logged = True

            # Input 1: Dataset Name
            self.dataset_name = st.text_input("Name of the dataset:", placeholder="e.g., Customer Transactions")

            
            # Input 2: Number of features
            if "feature_count" not in st.session_state:
                st.session_state.feature_count = 2

            for i in range(st.session_state.feature_count):
                feat = st.text_input(f"Feature {i + 1}", key=f"feature_{i}")
                self.features.append(feat)

            # Max features we can have is 5
            if st.session_state.feature_count < 5:
                if st.button("➕ Add Feature"):
                    st.session_state.feature_count += 1
                    st.rerun()

            
            # Input 3: Number of Datapoints
            self.num_rows = st.number_input("Number of rows:", min_value=1, step=10, value=100)
        

            st.divider()


            # Input 4: Output Feature            
            self.output_feature = st.text_input("Output Feature Name:", placeholder="e.g., Churn Status")
            

            # Input 5: Output feature type (numerical, categorical)
            self.feature_type = st.selectbox("Feature Type:", options=["Numerical", "Categorical"])

            
            # Input 6: Output Categories (if output feature type == categorical) 
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
            
        except Exception as e:
            raise CustomException(e, sys)
                    
        st.divider()



        try:
        
            is_submitted = st.button("Submit")
            
            if is_submitted:
                #st.write(f"**Dataset Name:** {self.dataset_name}")
                
                valid_features = [f for f in self.features if f.strip()]
                #st.write(f"**Features:** {valid_features}")
                #st.write(f"**Number of Data Points:** {self.num_rows}")
                #st.write(f"**Output Feature:** {self.output_feature}")
                #st.write(f"**Feature Type:** {self.feature_type}")
                
                #if self.feature_type == "Categorical":
                #    valid_categories = [c for c in self.output_categories if c.strip()]
                #    st.write(f"**Output Categories:** {valid_categories}")

                # Logs
                logging.info(f"Dataset Name: {self.dataset_name}")
                logging.info(f"Features: {self.features}")
                logging.info(f"Number of Rows: {self.num_rows}")
                logging.info(f"Output Feature: {self.output_feature}")
                logging.info(f"Output Feature Type: {self.feature_type}")
                logging.info(f"Output Categories: {self.output_categories}")
                logging.info("Data Ingestion Complete !")

            
            return self.dataset_name, self.features, self.num_rows, self.output_feature, self.feature_type, self.output_categories, is_submitted
            
        except Exception as e:
            raise CustomException(e, sys)
