import streamlit as st
import os
import PyPDF2
import re
from gensim.models.doc2vec import Doc2Vec
import numpy as np
from numpy.linalg import norm
from shutil import copyfile

def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()

    # Remove punctuation from the text
    text = re.sub('[^a-z]', ' ', text)

    # Remove numerical values from the text
    text = re.sub(r'\d+', '', text)

    # Remove extra whitespaces
    text = ' '.join(text.split())

    return text

def move_files(source_folder, destination_folder, threshold, jd_input):
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path) and filename.lower().endswith('.pdf'):
            pdf = PyPDF2.PdfFileReader(file_path)
            resume = ""
            for page_number in range(pdf.numPages):
                    page = pdf.getPage(page_number)
                    resume += page.extractText()

            input_cv = preprocess_text(resume)
            input_jd = preprocess_text(jd_input)

            # Model evaluation (Replace with your model loading code)
            model = Doc2Vec.load('D:/InfogenLabs/Resume TEst/GUI/GUI strimer/model/cv_job_maching.model')
            v1 = model.infer_vector(input_cv.split())
            v2 = model.infer_vector(input_jd.split())
            similarity = 100 * (np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1)) * norm(np.array(v2)))

            if similarity > threshold:
                destination_path = os.path.join(destination_folder, filename)
                copyfile(file_path, destination_path)

def main():
    st.title("JD Matcher App")

    # JD Input
    jd_input = st.text_area("Paste your JD here:")

    # User Input for Threshold
    threshold = st.slider("Select Similarity Threshold:", 0, 100, 70)

    # Select Input Folder
    input_folder = st.sidebar.selectbox("Select Input Folder", os.listdir("."))

    # Select Output Folder
    output_folder = st.sidebar.selectbox("Select Output Folder", os.listdir("."))

    # Match Button
    if st.button("Match and Move Resumes"):
        if os.path.exists(input_folder) and os.path.exists(output_folder):
            move_files(input_folder, output_folder, threshold, jd_input)
            st.success("Resumes moved successfully!")
        else:
            st.error("Please select valid input and output folders.")

if __name__ == "__main__":
    main()
