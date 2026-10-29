CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "customer_success_knowledge"
DEFAULT_TOP_K = 3


def get_chroma_collection(path=CHROMA_PATH, collection_name=COLLECTION_NAME):
    """Return a persistent Chroma collection for manual local testing."""
    import chromadb

    client = chromadb.PersistentClient(path=path)

    return client.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )


def format_chroma_results(results):
    """Normalize Chroma query results into context chunk dictionaries.

    Chroma query results often look like:
        {
            "ids": [["chunk-1"]],
            "documents": [["Text"]],
            "metadatas": [[{"source_id": "SRC-1"}]],
            "distances": [[0.12]]
        }
    """
    if not isinstance(results, dict):
        return []

    ids = (results.get("ids") or [[]])[0]
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    chunks = []

    for index, doc_id in enumerate(ids):
        text = documents[index] if index < len(documents) else None
        if not text or not text.strip():
            continue  # skip empty or missing docs

        metadata = metadatas[index] if index < len(metadatas) else None

        chunks.append(
            {
                "id": doc_id,
                "text": text.strip(),
                "source_id": metadata.get("source_id"),
                "title": metadata.get("title"),
                "category": metadata.get("category"),
                "section": metadata.get("section"),
                "distance": distances[index],
            }
        )

    return chunks


def retrieve_context(question, collection=get_chroma_collection(), top_k=DEFAULT_TOP_K):
    """Retrieve context chunks for a user question.

    Tests may pass a fake collection. Manual use should call Chroma.
    """
    question = question.strip()
    if not question:
        return []
    
    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return format_chroma_results(results)