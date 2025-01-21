"""Aggregate based on agents being equivalent based on the promises
in they require and provide, """

from collections import Counter
from typing import Optional


def aggrid(agent: dict) -> str:
    """Create an ID based on the values in provides and requires"""

    prov = sorted(agent["provides"])
    req = sorted(agent["requires"])
    return f"p:{'$$'.join(prov)}//r:{'$$'.join(req)}"


def assimilate(aggragent: Optional[dict], agentID: str, agent: dict) -> dict:
    """Assimilate a new agent into an existing aggregated agent. If the
    aggregated agent is None, just create a potensial aggregation from the
    new agent"""

    agent = agent.copy()
    if aggragent is None:
        agent["aggregated"] = [agentID]
        agent["name"] = "Aggr:\n   " + agent["name"]
        return agent
    aggragent["aggregated"].append(agentID)
    aggragent["name"] += "\n   " + agent["name"]
    aggragent["mitigations"] = list(
        set(aggragent["mitigations"]).union(set(agent["mitigations"]))
    )
    aggragent["relevant_for"] = list(
        set(aggragent["relevant_for"]).union(set(agent["relevant_for"]))
    )
    if "subagents" in agent:
        for subagentID, subagent in agent["subagents"].items():
            if subagentID not in aggragent["subagents"]:
                aggragent["subagents"][subagentID] = subagent
    aggragent["tactic"] = list(set(aggragent["tactic"]).union(set(agent["tactic"])))
    for ID in aggragent["aggregated"]:
        if ID.startswith("p"):
            print(aggragent)
            raise ValueError("double aggr")
    return aggragent


def create_aggregated_agents(agents: dict) -> dict:
    """create new aggregated agents from an existing agents dictionary,
    based on the agents having the same effect on a simulation from having
    the same provides and requires lists."""

    for agent_id in list(agents.keys()):
        agent = agents[agent_id]
        if aggrid(agent) in agents:
            aggragent = agents[aggrid(agent)]
            aggragent = assimilate(aggragent, agent_id, agent)
        else:
            aggragent = assimilate(None, agent_id, agent)
        agents[aggrid(agent)] = aggragent

    # remove any potensial aggregations that only contains the original
    # agent (no more than one agent has been aggregated to this ID)
    for agent_id in list(agents.keys()):
        agent = agents[agent_id]
        if "aggregated" in agent and len(agent["aggregated"]) <= 1:
            agents.pop(agent_id)
    return agents


def aggregate(agents: dict, data: Counter) -> Counter:
    """Aggregate the simulation based on the agents being equivalent"""

    agents = create_aggregated_agents(agents)

    c: Counter = Counter()

    for sim, n in data.items():
        newsim = set()
        for agentID in sim:
            agent = agents[agentID]
            if aggrid(agent) in agents:
                newsim.add(aggrid(agent))
            else:
                newsim.add(agentID)
        c[frozenset(newsim)] += n

    return c
