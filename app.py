from flask import Flask, jsonify, request

from lib.model_client import ModelClientError
from lib.rag_service import answer_question
from lib.validation import validate_question_payload


def create_app():
    app = Flask(__name__)

    @app.post("/api/ask")
    def ask():
        json = request.get_json(silent=True)
        validated_question, validation_error = validate_question_payload(json)

        if not validated_question:
            return validation_error, 400

        try:
            result = answer_question(validated_question)
        except ModelClientError as err:
            return {"error": "model_service_error", "message": str(err)}, 502

        return result, 200

    return app


app = create_app()
