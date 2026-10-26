from agents.base import BaseAgent
from agents.registry import register
from core.llm import get_llm

@register
class SQLAgent(BaseAgent):
    name = 'sql'
    description = 'Generate read-only SQL Server queries (not executed)'
    keywords = ('sql', 'query', 'table', 'database')

    def run(self, request: str) -> str:
        response = get_llm().invoke(
            'You are a SQL Server specialist. Generate only read-only SELECT queries '
            'and explain them. Do not claim to execute SQL. '
            'Assume dbo.Customers(CustomerID, Name, Age, City).\nRequest: ' + request
        )
        return str(response.content)
