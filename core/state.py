from typing import TypedDict

class AgentState(TypedDict):
    user_request: str
    selected_agent: str
    result: str
