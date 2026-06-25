from langchain_core.tools import tool
from tavily import TavilyClient
import os

@tool
def search_tavily(query: str) -> str:
    """Search the web using Tavily for current information on a topic."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        return "Tavily API key is missing. Please configure TAVILY_API_KEY."
    
    client = TavilyClient(api_key=tavily_api_key)
    try:
        response = client.search(query=query, max_results=3)
        results = response.get("results", [])
        if not results:
            return "No results found."
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content')}\n")
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error running search: {str(e)}"
