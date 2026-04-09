import chromadb
from embeddings import get_embeddings, chunk_text
from ingestion import extract_text_from_pdf
import os

# creating a persistent chromadb client
client = chromadb.PersistentClient(path="data/")

# create or load a collection
collection = client.get_or_create_collection(name="resumes")


def store_resume(pdf_path, candidate_name):
    """
    Takes a resume PDF and candidate name.
    Extracts text, chunks it, embeds it, stores in ChromaDB.
    """
    print(f"Processing resume for: {candidate_name}")

    text = extract_text_from_pdf(pdf_path)
    print(f"✓ Text extracted - {len(text)} chars")

    chunks = chunk_text(text)
    print(f"✓ Chunks created - {len(chunks)} chunks")

    vectors = get_embeddings(chunks)
    print(f"✓ Embeddings created - {len(vectors)} vectors")

    ids = [f"{candidate_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"candidate_name": candidate_name, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=vectors.tolist(),
        metadatas=metadatas
    )
    print("✓ Stored in ChromaDB successfully!")


def search_resumes(query, top_k=3):
    """
    Takes a search query from HR.
    Returns top_k most relevant resume chunks.
    """
    print(f"\nSearching for: {query}")

    query_vector = get_embeddings([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return results


def get_candidate_results(query, top_k=10):
    """
    Smarter search - groups chunks by candidate
    and returns ranked candidates with scores.
    """
    print(f"\nHR Query: {query}")

    raw_results = search_resumes(query, top_k=top_k)

    candidates = {}

    for i in range(len(raw_results["documents"][0])):
        name     = raw_results["metadatas"][0][i]["candidate_name"]  # ← [i] not [1]
        chunk    = raw_results["documents"][0][i]
        distance = raw_results["distances"][0][i]

        score = round((1 - distance / 2) * 100, 2)

        if name not in candidates:
            candidates[name] = {
                "name": name,
                "chunks": [],
                "scores": [],
                "best_score": 0
            }

        # ← these MUST be outside the if block, at this indentation level
        candidates[name]["chunks"].append(chunk)
        candidates[name]["scores"].append(score)

        if score > candidates[name]["best_score"]:
            candidates[name]["best_score"] = score

    # ← this MUST be outside the for loop
    for name in candidates:
        scores = candidates[name]["scores"]
        candidates[name]["avg_score"] = round(sum(scores) / len(scores), 2)

    ranked = sorted(candidates.values(), key=lambda x: x["best_score"], reverse=True)

    return ranked

def delete_candidate(candidate_name):
    """
    Removes all chunks of a candidate from ChromaDB.
    """
    # get all chunks in DB
    all_data = collection.get()

    # find IDs belonging to this candidate
    ids_to_delete = [
        id for id, meta in zip(all_data["ids"], all_data["metadatas"])
        if meta["candidate_name"] == candidate_name
    ]

    if not ids_to_delete:
        print(f"No data found for candidate: {candidate_name}")
        return False

    # delete them
    collection.delete(ids=ids_to_delete)
    print(f"✓ Deleted {len(ids_to_delete)} chunks for {candidate_name}")
    return True


# ← only ONE test block
if __name__ == "__main__":
    # store_resume("uploads/resume.pdf", "Shreyash")  ← commented out

    count = collection.count()
    print(f"Total chunks in DB: {count}")

    query = "Python machine learning developer with project experience"
    ranked_candidates = get_candidate_results(query, top_k=count)

    print("\n===== HR SHORTLIST RESULTS =====")
    for rank, candidate in enumerate(ranked_candidates, 1):
        print(f"\nRank #{rank} — {candidate['name']}")
        print(f"Best match score  : {candidate['best_score']} / 100")
        print(f"Average score     : {candidate['avg_score']} / 100")
        print(f"Relevant chunks   : {len(candidate['chunks'])}")
        print(f"Top chunk preview :")
        print(candidate['chunks'][0][:200])
        print("---")