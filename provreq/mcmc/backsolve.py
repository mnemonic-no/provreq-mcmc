"""Backsolver used to find possible 'ways' to the current list of agents"""

import argparse
import json
from typing import Dict, Set, Text

from provreq.tools import config


def command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments"""

    parser = config.common_args("AEP Cyberhunt Requirements backsolver")

    parser.add_argument(
        "-s", "--stats", type=str, default="stats.json", help="stats data"
    )

    parser.add_argument("--agents", type=config.split_arg, help="Agents to backsolve")

    args: argparse.Namespace = config.handle_args(parser, "generate")

    return args


def backsolve(
    stats: Dict[Text, Dict[Text, int]], agents: Dict[Text, Dict], base: Set[Text]
) -> Set[Text]:
    """find possible new set of agents"""

    reqs = set()
    for agent in base:
        for req in agents[agent]["requires"]:
            reqs.add(req)

    new_set = set()
    for req in reqs:
        max_agent = "NA"
        max_count = 0
        if req not in stats:
            print("can't find stats for requirement", req)
            continue
        for agentID, count in stats[req].items():
            if count > max_count:
                max_agent = agentID
                max_count = count
        if max_agent != "NA":
            new_set.add(max_agent)

    return new_set


def main() -> None:
    """main entry point"""

    args = command_line_arguments()

    with open(args.stats, encoding="utf8") as file_handle:
        stats = json.load(file_handle)

        agents, _, _ = config.read_agent_promises(args)

        new_agents: set = set(args.agents)
        base_agents = set(args.agents)

        while True:
            base_agents.update(new_agents)

            new_set = backsolve(stats, agents, base_agents)

            for agent in new_set.difference(base_agents):
                print(f"{agent} - {agents[agent]['name']}")

            new_agents.update(new_set)

            if not new_agents.difference(base_agents):
                break
            print("---")
