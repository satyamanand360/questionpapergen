import streamlit as st
import pdfplumber
from utils import extract_keywords, clean_text
from qg import (
    generate_question,
    generate_fill_in_blank,
    generate_true_false,
    generate_mcq,
    generate_match_columns,
)

st.set_page_config(page_title="Exam Paper Generator", layout="wide")
st.title("📝 Intelligent Exam Paper Generator")

input_mode = st.radio("Input Type", ["Topic", "Paste Text", "Upload PDF"])
question_type = st.selectbox("Question Type", ["MCQ", "Fill in the Blanks", "True/False", "Match the Columns"])

text = ""

if input_mode == "Topic":
    topic = st.text_input("Enter Topic")
    if topic:
        text = f"{topic} is an important concept in the curriculum."
elif input_mode == "Paste Text":
    text = st.text_area("Paste your notes or content here:")
elif input_mode == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF file")
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

if st.button("Generate Questions") and text:
    clean = clean_text(text)
    keywords = extract_keywords(clean, top_n=5)

    st.subheader("📋 Generated Questions")

    if question_type == "MCQ":
        for kw in keywords:
            q, opts, ans = generate_mcq(clean, kw)
            st.markdown(f"**Q:** {q}")
            for i, opt in enumerate(opts):
                st.markdown(f"- {chr(65+i)}. {opt}")
            st.markdown(f"**Answer:** `{ans}`\n---")

    elif question_type == "Fill in the Blanks":
        for kw in keywords:
            sent, ans = generate_fill_in_blank(clean, kw)
            st.markdown(f"**Q:** {sent}")
            st.markdown(f"**Answer:** `{ans}`\n---")

    elif question_type == "True/False":
        for kw in keywords:
            sent, label = generate_true_false(clean, kw)
            st.markdown(f"**Q:** {sent}")
            st.markdown(f"**Answer:** `{label}`\n---")

    elif question_type == "Match the Columns":
        pairs, answer_key = generate_match_columns(keywords)
        col1, col2 = zip(*pairs)
        st.markdown("**Column A** | **Column B**")
        st.markdown("---|---")
        for a, b in zip(col1, col2):
            st.markdown(f"{a} | {b}")
        st.markdown("**Answer Key:**")
        for k, v in answer_key.items():
            st.write(f"{k} → {v}")
