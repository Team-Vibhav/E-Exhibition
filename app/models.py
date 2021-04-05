from pydantic import BaseModel


class ContextQuery(BaseModel):
    question: str
    context_key: str


class CreateContext(BaseModel):
    context_key: str
    new_context: str
