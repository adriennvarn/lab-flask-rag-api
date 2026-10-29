def format_context_chunk(chunk):
    """Format one retrieved chunk for the prompt context block."""
    return f"""
    Source ID: {chunk['source_id']}
    Title: {chunk['title']}
    Category: {chunk['category']}
    Section: {chunk['section']}
    Text: {chunk['text']}
    """


def build_rag_prompt(question, context_chunks):
    """Build a structured RAG prompt from a question and retrieved context."""
    question = question.strip()
    if not question:
        raise ValueError("Question must not be blank.")

    #  Make sure at least some chunks have usable text
    usable_chunks = []
    for chunk in context_chunks:
        if chunk["text"].strip():
            usable_chunks.append(chunk)

    if not usable_chunks:
        raise ValueError("No usable chunks")

    context = "\n\n".join(format_context_chunk(chunk) for chunk in usable_chunks)

    prompt = f"""
    Instructions: You are a customer support assistant.
    Use only approved context documents below to generate your answer.
    Do not invent any information not supported by the context documents.
    If the context does not cover the question, say:
    "There is not enough information in the documentation for me to answer that question."
    
    Context:
    {context}
    
    Question:
    {question}
    
    Response Requirements:
    Respond concisely, in no more than three sentences.
    Use professional language that a customer service agent could use.
    Reference the source ID for any source that you use.
    """.strip()

    return prompt
