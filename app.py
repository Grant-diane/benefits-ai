import streamlit as st
import cv2
import langchain
import boto3

def main():

    st.set_page_config("Benefits AI")

    st.header("Benefits AI OCR")

    picture = st.camera_input("Take a picture")
    
    if picture is not None:
        img = cv2.imread(picture)

    if img:
        st.image(img)
        
if __name__ == "__main__":
    main()