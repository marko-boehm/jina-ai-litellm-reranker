import os
from typing import List, Dict, Any, Union
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
import json

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Jina AI Reranker Compatible API",
    description="A FastAPI implementation compatible with Jina AI Reranker API",
    version="1.0.0"
)

# Load configuration from environment variables
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "rerank-english-v3.0")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-1234")
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://0.0.0.0:4000")

# Create an HTTP client for making requests
http_client = httpx.AsyncClient()

class RerankRequest(BaseModel):
    model: str = RERANKER_MODEL
    query: str
    documents: List[str]
    top_n: int = None
    return_documents: bool = False

class RerankResult(BaseModel):
    index: int
    relevance_score: float
    document: Dict[str, Any] = None

class RerankResponse(BaseModel):
    results: List[RerankResult]

@app.post("/rerank", response_model=RerankResponse)
async def rerank_documents(request: RerankRequest):
    """
    Rerank documents based on their relevance to a query.
    
    Compatible with Jina AI Reranker API specification.
    """
    try:
        # Prepare the payload for LiteLLM
        payload = {
            #"model": request.model,
            "model": RERANKER_MODEL,  # Use the model specified in environment variable
            "query": request.query,
            "documents": request.documents,
        }
        
        # Add top_n if provided
        if request.top_n is not None:
            payload["top_n"] = request.top_n

        # Set up headers for authentication
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LITELLM_API_KEY}",
        }

        # Call the LiteLLM rerank endpoint
        response = await http_client.post(
            f"{LITELLM_BASE_URL}/rerank",
            json=payload,
            headers=headers,
        )
        
        # Raise an HTTP error if the call was not successful
        response.raise_for_status()

        # Parse the JSON response from LiteLLM
        result = response.json()
        
        # Map the response to Jina AI rerank API response format
        results = []
        for i, item in enumerate(result.get("results", [])):
            # Create the base result object
            rerank_result = RerankResult(
                index=item.get("index", i),
                relevance_score=item.get("relevance_score", 0.0)
            )
            
            # Add document only if return_documents is True
            if request.return_documents:
                rerank_result.document = {"text": request.documents[item.get("index", i)]}
                
            results.append(rerank_result)
            
        return RerankResponse(results=results)
        
    except httpx.HTTPStatusError as e:
        # Propagate errors coming from the rerank service
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error from rerank service: {e.response.text}",
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Error processing rerank request: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

# Close the HTTP client when the app shuts down
@app.on_event("shutdown")
async def close_http_client():
    await http_client.aclose()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)