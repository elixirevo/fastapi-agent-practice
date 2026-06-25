from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.agent import get_agent_executor
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

router = APIRouter()
agent_executor = get_agent_executor()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert request schemas to LangChain messages
        langchain_messages = []
        for msg in request.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported role: {msg.role}")
        
        # Invoke LangGraph agent
        result = await agent_executor.ainvoke({
            "messages": langchain_messages,
            "user_id": request.user_id
        })
        
        # Get the last AI message
        last_message = result["messages"][-1]
        
        return ChatResponse(
            role="assistant",
            content=last_message.content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
