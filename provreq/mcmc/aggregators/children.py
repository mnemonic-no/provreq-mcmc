"""Aggregate a set of simulations based on primary agent"""

from collections import Counter


def aggregate(_: dict, data: Counter) -> Counter:
    """aggregate a result to its parent agent if it is a subagent"""

    c: Counter = Counter()

    for sim, n in data.items():
        newsim = set()
        for agent in sim:
            newsim.add(agent.split(".")[0])
        c[frozenset(newsim)] += n

    return c
