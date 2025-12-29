from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from chroma_client import search_query
from prompt_template import build_prompt
from generate import generate_answer

app = FastAPI(
    title="MMR Statistics AI API",
    version="1.0"
)

# ---------------------------
# REQUEST MODELS
# ---------------------------
class SearchRequest(BaseModel):
    query: str
    k: int = 5
    region: Optional[str] = None
    industryId: Optional[str] = None


class GenerateRequest(BaseModel):
    query: str
    k: int = 5
    region: Optional[str] = None
    industryId: Optional[str] = None


# ---------------------------
# ROOT ENDPOINT
# ---------------------------
@app.get("/")
def root():
    return {"status": "MMR Statistics API is running"}


# ---------------------------
# SEARCH ENDPOINT
# ---------------------------
@app.post("/search")
def search(req: SearchRequest):
    filters = {}

    if req.region:
        filters["region"] = req.region
    if req.industryId:
        filters["industryId"] = req.industryId

    results = search_query(
        query=req.query,
        k=req.k,
        filters=filters if filters else None
    )

    return {
        "query": req.query,
        "filters": filters,
        "results_count": len(results),
        "results": results
    }


# ---------------------------
# GENERATE ENDPOINT
# ---------------------------
@app.post("/generate")
def generate(req: GenerateRequest):
    filters = {}

    if req.region:
        filters["region"] = req.region
    if req.industryId:
        filters["industryId"] = req.industryId

    results = search_query(
        query=req.query,
        k=req.k,
        filters=filters if filters else None
    )

    prompt = build_prompt(req.query, results)
    answer = generate_answer(prompt)

    return {
        "query": req.query,
        "filters": filters,
        "answer": answer,
        "sources": results
    }
