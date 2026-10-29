from lib.model_client import ModelClientError, generate_answer
from lib.prompt_builder import build_rag_prompt
from lib.response_formatter import (
    format_fallback_response,
    format_sources,
    format_success_response,
)
from lib.retrieval import DEFAULT_TOP_K, retrieve_context


def answer_question(
    question,
    retriever=None,
    prompt_builder=None,
    model_client=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the full RAG workflow for a validated question."""
    #  Use real calls by default
    retriever = retriever or retrieve_context
    prompt_builder = prompt_builder or build_rag_prompt
    model_client = model_client or generate_answer
    
    context = retriever(question, top_k=top_k)
    if not context:
        return format_fallback_response()
    
    prompt = prompt_builder(question, context)
    try:
        answer = model_client(prompt)
    except Exception as err:
        raise ModelClientError() from err
    
    if not answer or not answer.strip():
        raise ModelClientError()
    
    return format_success_response(answer, format_sources(context))