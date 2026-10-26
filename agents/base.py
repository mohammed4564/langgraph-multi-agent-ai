from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name: str
    description: str
    keywords: tuple[str, ...]

    @abstractmethod
    def run(self, request: str) -> str:
        """Execute the agent and return a textual result."""
