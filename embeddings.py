from sentence_transformers import SentenceTransformer
from langchain_text_splitters import  RecursiveCharacterTextSplitter


# load the embedding model
# first run = downloads ~90MB from HuggingFace
# after that = loads instantly from cache
model = SentenceTransformer('all-MiniLM-L6-v2')


def chunk_text(text , chunk_size=500 , chunk_overlap=100):
    """
    Splits resume into smaller overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap)
    
    chunks = splitter.split_text(text)
    return chunks

def get_embeddings(chunks):
    """
    Takes the list of chunks
    Returns one vector per chunk - each vector has 384 numbers.
    """
    vector = model.encode(chunks)
    return vector

# test block
if __name__ == "__main__":
    from ingestion import extract_text_from_pdf

    # step 1 — extract text
    text = extract_text_from_pdf("uploads/resume.pdf")
    print("✓ Text extracted — total chars:", len(text))

    # step 2 — chunk it
    chunks = chunk_text(text)
    print("✓ Chunks created:", len(chunks))
    print("\nFirst chunk preview:")
    print(chunks[0])
    print("\nSecond chunk preview:")
    print(chunks[1])

    # step 3 — embed
    vectors = get_embeddings(chunks)
    print("\n✓ Embeddings done")
    print("Total vectors:", len(vectors))
    print("Each vector size:", len(vectors[0]))
    print("\nFirst 10 numbers of first vector:")
    print(vectors[0][:10])