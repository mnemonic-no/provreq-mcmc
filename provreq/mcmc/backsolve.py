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

    parser.add_argument(
        "--techs", type=config.split_arg, help="Techniuqes to backsolve"
    )

    args: argparse.Namespace = config.handle_args(parser, "generate")

    return args


def backsolve(
    stats: Dict[Text, Dict[Text, int]], agents: Dict[Text, Dict], base: Set[Text]
) -> Set[Text]:
    """find possible new set of agents"""

    reqs = set()
    for tech in base:
        for req in agents[tech]["requires"]:
            reqs.add(req)

    new_set = set()
    for req in reqs:
        max_tech = "NA"
        max_count = 0
        if req not in stats:
            print("can't find stats for requirement", req)
            continue
        for techID, count in stats[req].items():
            if count > max_count:
                max_tech = techID
                max_count = count
        if max_tech != "NA":
            new_set.add(max_tech)

    return new_set


def main() -> None:
    """main entry point"""

    args = command_line_arguments()

    with open(args.stats, encoding="utf8") as file_handle:
        stats = json.load(file_handle)

        agents, _, _ = config.read_agent_promises(args)

        new_techs: set = set(args.techs)
        base_techs = set(args.techs)

        while True:
            base_techs.update(new_techs)

            new_set = backsolve(stats, agents, base_techs)

            for tech in new_set.difference(base_techs):
                print(f"{tech} - {agents[tech]['name']}")

            new_techs.update(new_set)

            if not new_techs.difference(base_techs):
                break
            print("---")
