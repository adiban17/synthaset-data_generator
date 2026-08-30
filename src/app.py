import sys
from src.exception import CustomException
from src.logger import logging
from src.config import Config
from src.utils import clean_output
import streamlit as st
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_classification import DataClassification

dataingestion = DataIngestion()

st.title("SynthSet POC")
st.subheader("Dataset Configuration")

dataset_name, features, num_rows, output_feature, output_type, feature_categories, is_submitted = dataingestion.ingest_data()

if is_submitted:
    datavalidation = DataValidation(
        dataset_name=dataset_name,
        features=features,
        num_rows=num_rows,
        output_feature=output_feature,
        output_type=output_type,
        feature_categories=feature_categories
    )
    
    with st.spinner("Agent is validating your features..."):
        is_relevant, reasoning = datavalidation.data_validation()


    
    if is_relevant:
        dataclassification = DataClassification(
            dataset_name=dataset_name,
            features=features
        )

        with st.spinner("Agent is classifying your features..."):
            numerical_features, categoircal_features = dataclassification.data_classification()
    else:
        st.write('Try Again with a valid configuration')


# Fixed tuple unpacking here
#is_relevant, reasoning = datavalidation.data_validation()

#st.divider() # Adds a clean horizontal line
#st.subheader("Validation Results")

# Display a colored alert based on whether the validation passed or failed
#if is_relevant:
#    st.success("✅ Validation Passed: All features are relevant.", icon="✅")
#else:
#    st.error("❌ Validation Failed: Irrelevant or mismatched features detected.", icon="🚨")

# Put the verbose reasoning inside a clean container
#with st.expander("View Detailed Reasoning", expanded=True):
#    st.markdown(f"**Agent Reasoning:**\n\n{reasoning}")





# If you want to keep the old logic for reference without it displaying on screen,
# use the '#' symbol for each line like this:

# user_query = st.text_input("Ask:", placeholder="e.g., What is the full form of BBC?")
# logging.info(f"User Query:{user_query}")
#
# try:
#     if st.button("Shoot"):
#         if user_query:
#             with st.spinner("Thinking..."):
#                 result = agent.invoke({"messages": [("user", user_query)]})
#                 answer = clean_output(result)
#                 logging.info(f"Response:{answer}")
#                 st.write("**Response:**")
#                 st.info(answer)
#         else:
#             st.warning("Please enter a question first.")
# except Exception as e:
#     raise CustomException(e, sys)