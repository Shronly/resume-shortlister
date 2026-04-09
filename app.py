import streamlit as st
from retrieval import store_resume, get_candidate_results, collection, delete_candidate
from ranker import rank_candidates_with_llm
import tempfile
import os

# page config
st.set_page_config(
    page_title="Resume Shortlister AI",
    page_icon="🤖",
    layout="wide"
)

# title
st.title("🤖 Resume Shortlister AI")
st.markdown("*Powered by RAG + LLM — upload resumes, search by requirements*")
st.divider()

# two columns layout
col1, col2 = st.columns([1, 1])

# ─── LEFT COLUMN — Upload + Delete ───
with col1:
    st.subheader("📄 Upload Resume")

    candidate_name = st.text_input(
        "Candidate Name",
        placeholder="e.g. Shreyash Aryaa"
    )

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    if st.button("Upload Resume", type="primary"):
        if not candidate_name:
            st.error("Please enter candidate name!")
        elif uploaded_file is None:
            st.error("Please upload a PDF file!")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            with st.spinner(f"Processing {candidate_name}'s resume..."):
                try:
                    store_resume(tmp_path, candidate_name)
                    st.success(f"✅ {candidate_name}'s resume uploaded successfully!")
                    total = collection.count()
                    st.info(f"Total resumes in database: {total // 5}")
                except Exception as e:
                    if "already exists" in str(e):
                        st.warning(f"⚠️ {candidate_name}'s resume already exists in DB!")
                    else:
                        st.error(f"Error: {str(e)}")

            os.unlink(tmp_path)

    # ─── Delete Section ───
    st.divider()
    st.subheader("🗑️ Remove Candidate")

    delete_name = st.text_input(
        "Candidate name to remove",
        placeholder="e.g. Shreyash Aryaa"
    )

    if st.button("Remove Candidate", type="secondary"):
        if not delete_name:
            st.error("Please enter candidate name!")
        else:
            with st.spinner(f"Removing {delete_name}..."):
                success = delete_candidate(delete_name)
                if success:
                    st.success(f"✅ {delete_name} removed from database!")
                else:
                    st.warning(f"⚠️ No candidate found with name: {delete_name}")

    # ─── DB Stats ───
    st.divider()
    st.subheader("📊 Database Stats")
    total_chunks  = collection.count()
    total_resumes = total_chunks // 5
    st.metric("Resumes in Database", total_resumes)
    st.metric("Total Chunks Stored", total_chunks)


# ─── RIGHT COLUMN — HR Search ───
with col2:
    st.subheader("🔍 Search Candidates")

    query = st.text_area(
        "Job Requirement",
        placeholder="e.g. Python machine learning developer with project experience and knowledge of TensorFlow",
        height=120
    )

    top_candidates = st.slider(
        "Number of top candidates to analyze",
        min_value=1,
        max_value=10,
        value=3
    )

    if st.button("🔍 Find Candidates", type="primary"):
        if not query:
            st.error("Please enter a job requirement!")
        elif collection.count() == 0:
            st.error("No resumes in database! Please upload some first.")
        else:
            with st.spinner("Searching and analyzing candidates..."):
                count = collection.count()
                ranked_candidates = get_candidate_results(query, top_k=count)
                final_results = rank_candidates_with_llm(
                    query,
                    ranked_candidates[:top_candidates]
                )

            st.divider()
            st.subheader("📋 Shortlist Results")

            for rank, candidate in enumerate(final_results, 1):
                score = candidate["score"]
                if score >= 50:
                    color = "🟢"
                elif score >= 30:
                    color = "🟡"
                else:
                    color = "🔴"

                with st.expander(
                    f"{color} Rank #{rank} — {candidate['name']} | Score: {score}/100",
                    expanded=True
                ):
                    st.markdown(f"**Match Score:** {score}/100")
                    st.markdown("**AI Analysis:**")
                    st.markdown(candidate['analysis'])