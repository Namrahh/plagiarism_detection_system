
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def classify_similarity(score):
    if score < 15:
        return "Low similarity"
    elif score < 24:
        return "Moderate similarity"
    else:
        return "High similarity"


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
            text = file.read().decode(
                "utf-8",
                errors="ignore"
            )

            documents[file.name] = text

        results_df = compare_documents(documents)

        st.subheader("Similarity Results")

        st.dataframe(
            results_df,
            use_container_width=True
        )

        csv = results_df.to_csv(index=False)

        st.download_button(
            label="Download Results CSV",
            data=csv,
            file_name="plagiarism_results.csv",
            mime="text/csv"
        )
