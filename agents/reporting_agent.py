from agents.base import BaseAgent
from agents.registry import register
from core.llm import get_llm

@register
class ReportingAgent(BaseAgent):
    name = 'report'
    description = 'Draft a general data engineering report'
    keywords = ('report', 'summary', 'summarize', 'documentation')

    def run(self, request: str) -> str:
        response = get_llm().invoke(
            'You are a reporting specialist. Write a concise report. '
            'You have no access to other agent outputs; do not invent measurements.\nRequest: ' + request
        )
        return str(response.content)
