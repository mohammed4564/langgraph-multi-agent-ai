import importlib
import pkgutil
from agents.base import BaseAgent

AGENTS: dict[str, BaseAgent] = {}

def register(cls: type[BaseAgent]):
    if not issubclass(cls, BaseAgent):
        raise TypeError('Agent must inherit BaseAgent')
    instance = cls()
    if not instance.name or instance.name in AGENTS:
        raise ValueError(f'Missing or duplicate agent name: {instance.name}')
    AGENTS[instance.name] = instance
    return cls

def discover():
    import agents
    for module in pkgutil.iter_modules(agents.__path__):
        if module.name not in {'base', 'registry'} and not module.name.startswith('_'):
            importlib.import_module(f'agents.{module.name}')
    return AGENTS
