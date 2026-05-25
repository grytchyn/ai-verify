import httpx
import asyncio
from typing import List, Dict, Any

def sync_search_web(query: str, limit: int = 3) -> List[Dict]:
    """
    Simple wrapper around DuckDuckGo Instant Answer API.
    Returns list of dicts with keys: title, url, snippet.
    """
    # Use httpx in a sync way via asyncio.run
    return asyncio.run(_async_search_web(query, limit))

async def _async_search_web(query: str, limit: int) -> List[Dict]:
    """
    Async search using DuckDuckGo Instant Answer API.
    Returns list of results with title, url, snippet.
    """
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            
        results = []
        # RelatedTopics may contain nested structures; we'll extract simple ones.
        for topic in data.get("RelatedTopics", []):
            if isinstance(topic, dict) and topic.get("FirstURL") and topic.get("Text"):
                results.append({
                    "title": topic.get("Text")[:100],
                    "url": topic.get("FirstURL"),
                    "snippet": topic.get("Text")[:200]
                })
            if len(results) >= limit:
                break
                
        # If not enough, fallback to Abstract
        if not results and data.get("Abstract"):
            results.append({
                "title": data.get("Heading") or query,
                "url": data.get("AbstractURL") or "",
                "snippet": data.get("Abstract")[:300]
            })
            
        return results[:limit]
    except Exception as e:
        # Return empty list on failure
        print(f"Search error: {e}")
        return []

# Add compatibility function for main.py
def duckduckgo_instant_answer(query: str) -> List[Dict]:
    """
    Simple wrapper around DuckDuckGo Instant Answer API.
    Returns list of results with 'content'.
    """
    # Use sync version of search
    results = sync_search_web(query, limit=3)
    # Convert to expected format (with 'content' key)
    converted = []
    for r in results:
        converted.append({
            "content": f"{r.get('title', '')}. {r.get('snippet', '')}"
        })
    return converted