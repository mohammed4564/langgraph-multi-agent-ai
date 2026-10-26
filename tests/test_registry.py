from agents.registry import discover

def test_discovery():
    agents = discover()
    assert {'sql', 'quality', 'report'} <= set(agents)

def test_agent_metadata():
    for name, agent in discover().items():
        assert agent.name == name
        assert agent.description
        assert agent.keywords
