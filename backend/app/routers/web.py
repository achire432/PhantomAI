from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.app.dependencies.auth import get_current_user
from backend.app.models.user import User
from backend.app.services.tools import search_web
from backend.app.services.web_reader import read_webpage
from backend.app.services.web_research import summarize_webpage_with_ai, ask_webpage_with_ai, research_web_with_ai

router = APIRouter(prefix="/web", tags=["Web Search"])


class WebSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    max_results: int = Field(default=8, ge=1, le=20)


class WebReadRequest(BaseModel):
    url: str = Field(..., min_length=1)
    max_characters: int = Field(default=15000, ge=1000, le=50000)


class WebSummarizeRequest(BaseModel):
    url: str = Field(..., min_length=1)
    max_characters: int = Field(default=15000, ge=1000, le=50000)


class WebAskRequest(BaseModel):
    url: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    max_characters: int = Field(default=15000, ge=1000, le=50000)


class WebResearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    max_results: int = Field(default=5, ge=1, le=10)
    max_characters_per_source: int = Field(default=8000, ge=1000, le=20000)


@router.get("/search")
def web_search(
    query: str,
    max_results: int = 8,
    current_user: User = Depends(get_current_user),
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    if max_results < 1 or max_results > 20:
        raise HTTPException(status_code=400, detail="max_results must be between 1 and 20.")

    result = search_web(query=query.strip(), max_results=max_results)

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Web search failed."),
        )

    return result


@router.post("/search")
def web_search_post(
    request: WebSearchRequest,
    current_user: User = Depends(get_current_user),
):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    result = search_web(
        query=query,
        max_results=request.max_results,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Web search failed."),
        )

    return result


@router.post("/read")
def read_web(
    request: WebReadRequest,
    current_user: User = Depends(get_current_user),
):
    url = request.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    result = read_webpage(url)

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unable to read webpage."),
        )

    result["text"] = result.get("text", "")[:request.max_characters]

    return result


@router.post("/summarize")
def summarize_webpage(
    request: WebSummarizeRequest,
    current_user: User = Depends(get_current_user),
):
    url = request.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    result = summarize_webpage_with_ai(
        url=url,
        max_characters=request.max_characters,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unable to summarize webpage."),
        )

    return result


@router.post("/ask")
def ask_webpage(
    request: WebAskRequest,
    current_user: User = Depends(get_current_user),
):
    url = request.url.strip()
    question = request.question.strip()

    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    result = ask_webpage_with_ai(
        url=url,
        question=question,
        max_characters=request.max_characters,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Unable to answer question."),
        )

    return result


@router.post("/research")
def research_web(
    request: WebResearchRequest,
    current_user: User = Depends(get_current_user),
):
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="Research query cannot be empty.")

    result = research_web_with_ai(
        query=query,
        max_results=request.max_results,
        max_characters_per_source=request.max_characters_per_source,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Web research failed."),
        )

    return result
