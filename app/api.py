import logging
from fastapi import FastAPI, HTTPException, Header

from transformers import pipeline

from app import config
from app import models

contexts = config.CONTEXTS

logger = logging.getLogger(__name__)

model_name = "deepset/roberta-base-squad2"
nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

MAX_LEN = 320

app = FastAPI()


@app.get("/")
async def index_page():
    """
    Index page
    """
    return "Question Answering API for E-Exhibition"


@app.post("/predict")
async def predict(query: models.ContextQuery):
    """
    Returns answer for a question, with the context that is saved with the given context key
    """

    question = query.question
    context_key = query.context_key

    if context_key in contexts:
        QA_input = {"question": question, "context": contexts[context_key]}
    else:
        raise HTTPException(status_code=400, detail="Invalid context query")

    prediction = nlp(QA_input)

    if prediction["score"] > config.SCORE_THRESHOLD:
        return prediction
    else:
        return "Change The Question Please."


@app.post("/contexts")
async def add_context(context: models.CreateContext, x_auth_key: str = Header(None)):
    """
    Add or update a context with the given context key
    """

    logger.info("Auth Key : %s", x_auth_key)
    logger.info("Context : %s", context)

    if config.DEV_PASSWORD != x_auth_key:
        raise HTTPException(status_code=403, detail="Unauthorized")

    context_key = context.context_key
    new_context = context.new_context

    contexts[context_key] = new_context

    return "Context Changed Successfully"


@app.get("/contexts")
async def show_contexts(x_auth_key: str = Header(None)):
    """
    Get current contexts
    """

    if config.DEV_PASSWORD != x_auth_key:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return contexts