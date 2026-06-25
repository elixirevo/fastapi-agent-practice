from langchain_core.tools import tool
from tavily import TavilyClient
import os
from sqlmodel import select
from app.core.database import get_session
from app.models.user_interest import UserInterest

@tool
async def save_user_interest(user_id: str, interest: str) -> str:
    """Save a specific interest or hobby for a user.
    Use this tool when the user mentions something they like, are interested in, or want you to remember.
    """
    try:
        async with get_session() as session:
            statement = select(UserInterest).where(
                UserInterest.user_id == user_id,
                UserInterest.interest == interest
            )
            result = await session.execute(statement)
            existing = result.scalar_one_or_none()
            
            if not existing:
                new_interest = UserInterest(user_id=user_id, interest=interest)
                session.add(new_interest)
                await session.commit()
                return f"Successfully saved interest '{interest}' for user '{user_id}'."
            else:
                return f"Interest '{interest}' already exists for user '{user_id}'."
    except Exception as e:
        return f"Error saving interest: {str(e)}"

@tool
async def get_user_interests(user_id: str) -> str:
    """Retrieve all saved interests for a specific user.
    Use this tool to load user preferences and personalize responses.
    """
    try:
        async with get_session() as session:
            statement = select(UserInterest).where(UserInterest.user_id == user_id)
            result = await session.execute(statement)
            interests_objects = result.scalars().all()
            
        if not interests_objects:
            return f"No interests found for user '{user_id}'."
        
        interests = [item.interest for item in interests_objects]
        return f"User '{user_id}' has the following interests: {', '.join(interests)}"
    except Exception as e:
        return f"Error retrieving interests: {str(e)}"

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

