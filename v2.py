import streamlit as st
import PyPDF2
import re
from gensim.models.doc2vec import Doc2Vec
import numpy as np
from numpy.linalg import norm

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

def main():
    st.title("JD Matcher App")

    # JD Input
    jd_input = st.text_area("Paste your JD here:")

    # Load CV Button
    cv_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])

    # Match Button
    if st.button("Match CV with JD"):
        if cv_file is not None:
            pdf = PyPDF2.PdfFileReader(cv_file)
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

            st.success(f"Similarity: {round(similarity, 2)}%")
        else:
            st.error("Please upload a CV (PDF) file.")

if __name__ == "__main__":
    main()
