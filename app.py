from fastapi import FastAPI
from pydantic import BaseModel
from chroma_client import search_query
from generate import generate_answer, build_prompt

app = FastAPI()

class Req(BaseModel):
    query: str
    k: int = 5
    allowed_industries: list | None = None

@app.post("/search")
def search(req: Req):
    return search_query(req.query, k=req.k, allowed_industries=req.allowed_industries)

@app.post("/generate")
def generate(req: Req):
    results = search_query(req.query, k=req.k, allowed_industries=req.allowed_industries)
    prompt = build_prompt(req.query, results)
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": results
    }
