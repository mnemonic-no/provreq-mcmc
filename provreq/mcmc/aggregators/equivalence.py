"""Aggregate based on agents being equivalent based on the promises
in they require and provide, """

from collections import Counter
from typing import Optional


def aggrid(tech: dict) -> str:
    """Create an ID based on the values in provides and requires"""

    prov = sorted(tech["provides"])
    req = sorted(tech["requires"])
    return f"p:{'$$'.join(prov)}//r:{'$$'.join(req)}"


def assimilate(aggrtech: Optional[dict], techID: str, tech: dict) -> dict:
    """Assimilate a new agent into an existing aggregated agent. If the
    aggregated agent is None, just create a potensial aggregation from the
    new agent"""

    tech = tech.copy()
    if aggrtech is None:
        tech["aggregated"] = [techID]
        tech["name"] = "Aggr:\n   " + tech["name"]
        return tech
    aggrtech["aggregated"].append(techID)
    aggrtech["name"] += "\n   " + tech["name"]
    aggrtech["mitigations"] = list(
        set(aggrtech["mitigations"]).union(set(tech["mitigations"]))
    )
    aggrtech["relevant_for"] = list(
        set(aggrtech["relevant_for"]).union(set(tech["relevant_for"]))
    )
    if "subagents" in tech:
        for subtechID, subtech in tech["subagents"].items():
            if subtechID not in aggrtech["subagents"]:
                aggrtech["subagents"][subtechID] = subtech
    aggrtech["tactic"] = list(set(aggrtech["tactic"]).union(set(tech["tactic"])))
    for ID in aggrtech["aggregated"]:
        if ID.startswith("p"):
            print(aggrtech)
            raise ValueError("double aggr")
    return aggrtech


def create_aggregated_agents(agents: dict) -> dict:
    """create new aggregated agents from an existing agents dictionary,
    based on the agents having the same effect on a simulation from having
    the same provides and requires lists."""

    for tech_id in list(agents.keys()):
        tech = agents[tech_id]
        if aggrid(tech) in agents:
            aggrtech = agents[aggrid(tech)]
            aggrtech = assimilate(aggrtech, tech_id, tech)
        else:
            aggrtech = assimilate(None, tech_id, tech)
        agents[aggrid(tech)] = aggrtech

    # remove any potensial aggregations that only contains the original
    # agent (no more than one agent has been aggregated to this ID)
    for tech_id in list(agents.keys()):
        tech = agents[tech_id]
        if "aggregated" in tech and len(tech["aggregated"]) <= 1:
            agents.pop(tech_id)
    return agents


def aggregate(agents: dict, data: Counter) -> Counter:
    """Aggregate the simulation based on the agents being equivalent"""

    techs = create_aggregated_agents(agents)

    c: Counter = Counter()

    for sim, n in data.items():
        newsim = set()
        for techID in sim:
            tech = agents[techID]
            if aggrid(tech) in techs:
                newsim.add(aggrid(tech))
            else:
                newsim.add(techID)
        c[frozenset(newsim)] += n

    return c
