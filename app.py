import streamlit as st
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DynamoDB client
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = 'us-east-1'  # Mumbai region

dynamodb = boto3.resource(
    'dynamodb', 
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

table_name = 'user_data'  # Your DynamoDB table name
table = dynamodb.Table(table_name)

# Streamlit app UI
st.title('User Information Submission')

# Form for data entry
with st.form(key='user_form'):
    # Inputs for user data
    name = st.text_input("Name", value=st.session_state.get("name", ""))
    age = st.number_input("Age", min_value=0, value=st.session_state.get("age", 0))
    fav_hero = st.text_input("Favorite Hero", value=st.session_state.get("fav_hero", ""))
    job = st.text_input("Job", value=st.session_state.get("job", ""))

    # Button to submit the current data to DynamoDB
    submit_button = st.form_submit_button(label="Submit Data")

    # On Submit Data button click
    if submit_button:
        # Check if user already exists in DynamoDB
        response = table.get_item(
            Key={
                'user_id': name  # Assuming 'user_id' is the primary key in DynamoDB
            }
        )
        
        if 'Item' in response:
            # If the user already exists, show an error message
            st.error("User already exists. Please try with a different name.")
        else:
            # Save the form data to DynamoDB
            response = table.put_item(
                Item={
                    'user_id': name,  # Assuming 'user_id' is the primary key in DynamoDB
                    'name': name,
                    'age': age,
                    'fav_hero': fav_hero,
                    'job': job
                }
            )
            
            # Show success message
            st.success("Data submitted successfully!")
            
            # Store the data in session state
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.fav_hero = fav_hero
            st.session_state.job = job

            # Clear session state to reset form after submission
            st.session_state.clear()
            
            # Reset the page to allow for new submission
            st.experimental_rerun()
