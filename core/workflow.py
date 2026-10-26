from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from agents.registry import discover


def build_workflow():
    agents = discover()
    if not agents:
        raise RuntimeError('No agents registered')

    def supervisor(state: AgentState):
        request = state['user_request'].lower()
        scores = {
            name: sum(word in request for word in agent.keywords)
            for name, agent in agents.items()
        }
        # Deterministic routing is reliable with small local models.
        chosen = max(scores, key=scores.get)
        if scores[chosen] == 0:
            chosen = 'report' if 'report' in agents else next(iter(agents))
        return {'selected_agent': chosen}

    graph = StateGraph(AgentState)
    graph.add_node('supervisor', supervisor)
    for name, agent in agents.items():
        def run_agent(state: AgentState, selected=agent):
            return {'result': selected.run(state['user_request'])}
        graph.add_node(name, run_agent)
        graph.add_edge(name, END)
    graph.add_edge(START, 'supervisor')
    graph.add_conditional_edges(
        'supervisor',
        lambda state: state['selected_agent'],
        {name: name for name in agents},
    )
    return graph.compile()
