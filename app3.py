import streamlit as st
import cv2
import pytesseract
import pandas as pd
import numpy as np
import tempfile
import re

# Enhanced Function to Extract Text from Image
def extract_text(image):
    # Convert the image to RGB and Grayscale
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

    # Applying Gaussian blur and thresholding
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Custom Tesseract configuration
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789%&$#@-?:()/;,*.\' "'

    # OCR using Tesseract on the thresholded image
    text = pytesseract.image_to_string(thresh, config=custom_config)

    return text

# Function to Parse Extracted Text
def parse_extracted_text(text):
    name_regex = r"Name:\s*(.+)"
    dob_regex = r"DOB:\s*(\d{2}/\d{2}/\d{4})"
    address_regex = r"Address:\s*(.+)"
    name = re.search(name_regex, text)
    dob = re.search(dob_regex, text)
    address = re.search(address_regex, text)
    return {
        "Name": name.group(1) if name else "Not found",
        "DOB": dob.group(1) if dob else "Not found",
        "Address": address.group(1) if address else "Not found"
    }

# Main Streamlit Application
def main():
    st.title("ID Card Information Extractor")
    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(img_file_buffer.getvalue())
            image = cv2.imread(tmp.name)

        st.image(image, channels="BGR", caption="Captured Image")
        extracted_text = extract_text(image)
        if extracted_text.strip():
            st.write("Extracted Text:", extracted_text)
            parsed_data = parse_extracted_text(extracted_text)

            for key, value in parsed_data.items():
                st.write(f"{key}: {value}")

            if st.button("Save to sheet"):
                df = pd.DataFrame([parsed_data])
                df.to_csv("extracted_info.csv", mode='a', header=False, index=False)
                st.success("Saved to sheet")
        else:
            st.warning("No text could be extracted from the image.")

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.3.4_1/bin/tesseract"
    main()
