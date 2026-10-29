MIN_QUESTION_LENGTH = 3


def validate_question_payload(payload):
    """Validate the JSON body for POST /api/ask.

    Return:
        (question, None) when valid
        (None, error_dict) when invalid
    """
    # TODO: Require payload to be a dictionary.
    # TODO: Require a question field.
    # TODO: Require question to be a string.
    # TODO: Strip extra whitespace.
    # TODO: Reject blank questions.
    # TODO: Reject questions shorter than MIN_QUESTION_LENGTH.
    
    if not isinstance(payload, dict):
        return None, {"error": "invalid_request", "message": "str"}
    if "question" not in payload.keys():
        return None, {"error": "missing_question", "message": "str"}
    
    question = payload["question"]
    
    if not isinstance(question, str):
        return None, {"error": "invalid_question", "message": "str"}
    
    question = question.strip()
    
    if not question:
        return None, {"error": "empty_question", "message": "str"}
    if not len(question) >= MIN_QUESTION_LENGTH:
        return None, {"error": "short_question", "message": "str"}
    
    return (question, None)