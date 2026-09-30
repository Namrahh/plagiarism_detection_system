
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
from docx import Document

def classify_similarity(score):
    if score < 15:
        return "Low similarity"
    elif score < 24:
        return "Moderate similarity"
    else:
        return "High similarity"

def extract_text(file):

    if file.name.endswith(".txt"):
        return file.read().decode(
            "utf-8",
            errors="ignore"
        )

    elif file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif file.name.endswith(".docx"):
        document = Document(file)
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""
def compare_documents(documents):

    document_names = list(documents.keys())
    texts = list(documents.values())

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_percentage = similarity_matrix * 100

    results = []

    for i in range(len(document_names)):
        for j in range(i + 1, len(document_names)):

            score = round(similarity_percentage[i][j], 2)

            results.append({
                "Document 1": document_names[i],
                "Document 2": document_names[j],
                "Similarity (%)": score,
                "Result": classify_similarity(score)
            })

    results_df = pd.DataFrame(results)

    return results_df.sort_values(
        by="Similarity (%)",
        ascending=False
    ).reset_index(drop=True)


st.set_page_config(
    page_title="Plagiarism Detection",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Plagiarism Detection System")

st.write(
    "Upload two or more text documents to calculate their textual similarity."
)

uploaded_files = st.file_uploader(
    "Upload documents",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:

    if len(uploaded_files) < 2:
        st.warning("Please upload at least 2 documents.")

    else:

        documents = {}

        for file in uploaded_files:
            text = extract_text(file)
            documents[file.name] = text

        results_df = compare_documents(documents)

        st.subheader("Analysis Summary")

        total_documents = len(documents)

        high_count = (
            results_df["Result"] == "High similarity"
        ).sum()

        moderate_count = (
            results_df["Result"] == "Moderate similarity"
        ).sum()

        low_count = (
            results_df["Result"] == "Low similarity"
        ).sum()

        highest_similarity = results_df["Similarity (%)"].max()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Documents", total_documents)
        col2.metric("High Similarity", high_count)
        col3.metric("Moderate Similarity", moderate_count)
        col4.metric("Low Similarity", low_count)

        st.metric(
            "Highest Similarity",
            f"{highest_similarity:.2f}%"
        )

        # Most Similar Document Pair

        most_similar = results_df.iloc[0]

        st.subheader("Most Similar Document Pair")

        st.write(
            f"**{most_similar['Document 1']}** ↔ "
            f"**{most_similar['Document 2']}**"
        )

        st.metric(
            "Similarity",
            f"{most_similar['Similarity (%)']:.2f}%"
        )

        st.subheader("Similarity Results")

        st.dataframe(
            results_df,
            use_container_width=True
        )

        st.subheader("Similarity Chart")

        chart_data = results_df.set_index(
            results_df["Document 1"] + " vs " + results_df["Document 2"]
        )["Similarity (%)"]

        st.bar_chart(chart_data)

        csv = results_df.to_csv(index=False)

        st.download_button(
            label="Download Results CSV",
            data=csv,
            file_name="plagiarism_results.csv",
            mime="text/csv"
        )
