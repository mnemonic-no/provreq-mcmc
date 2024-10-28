"""montecarlo simulation used to find possible 'ways' to the current list of agents"""

import argparse
import datetime
import json
import logging
import os
import random
import signal
import sys
import types
from collections import Counter
from typing import Any, Dict, List, Optional, Set, Text

import tabulate
from provreq.tools import config
from provreq.tools.libs.libgenerate import simulate, stages_table

import provreq.mcmc.aggregators.children
import provreq.mcmc.aggregators.equivalence
from provreq.mcmc.pbar import ProgressBar

missing_counter: Counter = Counter()


def sigint_handler(sig: int, frame: Optional[types.FrameType]) -> Any:
    """show errors on ctrl-c"""

    if frame:
        print(frame)

    print(
        "Simulation ended due to signal",
        sig,
        "\n",
        "Simulations ending due to missing requirements.. (stats for runs that did not complete)",
    )

    print(
        tabulate.tabulate(
            missing_counter.items(), headers=["promise", "count"], tablefmt="fancy_grid"
        )
    )
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments"""

    parser = config.common_args("AEP Cyberhunt Requirements montecarlo")

    parser.add_argument(
        "-s", "--stats", type=str, default="stats.json", help="stats data"
    )

    parser.add_argument("--seeds", type=config.split_arg, help="Seeds of promises")

    parser.add_argument(
        "--hints",
        action="store_true",
        help="Create info of possible agents in place of seeds",
    )

    parser.add_argument(
        "--agents", type=config.split_arg, help="Agents to seed montecarlo"
    )

    parser.add_argument(
        "--top", type=int, default=5, help="number of results to show, default: 5"
    )

    parser.add_argument(
        "-a",
        "--aggregation",
        type=str,
        default="",
        help="Aggregate final simulation based [children, equivalence]",
    )

    parser.add_argument(
        "-r",
        "--runs",
        type=int,
        default=100_000,
        help="Number of simulated passes through the chain",
    )

    parser.add_argument(
        "--stop-agents",
        type=config.split_arg,
        help=(
            "Agents to stop simulation (default: "
            "all Initial Access agents)          "
        ),
    )

    parser.add_argument(
        "--stop-agent_class",
        type=str,
        help=(
            "Agents to stop simulation will be all of this agent_class"
            "(default: all Initial Access agent_class)"
        ),
    )

    parser.add_argument(
        "--pre-seed-stop-agent-requirements",
        action="store_true",
        help=(
            "Add all requirements of the stop agents to the seed list."
            "This will allow for stopping on agents more in the middle of"
            "the attack chain, which would otherwise be in-accessible due to missing"
            "agents in the chain up to that point."
        ),
    )

    parser.add_argument(
        "--seed-class",
        type=config.split_arg,
        help=("Populate seed agent list with all agents of one (or more) classes"),
    )

    args: argparse.Namespace = config.handle_args(parser, "generate")

    return args


def sample_agent(
    agent: Text,
    agents: Dict[Text, Dict],
    expanded_stats: Dict[Text, List[Text]],
    allready_provided: Optional[set] = None,
) -> List[Text]:
    """Select agents that provides all requires of the agent based on probability"""

    to_fullfill = set(agents[agent]["requires"])
    if allready_provided:
        to_fullfill -= allready_provided

    res = []
    while to_fullfill:
        prom = to_fullfill.pop()
        if prom not in expanded_stats:
            # logging.warning("Promises never seen in stats %s", prom)
            return []
        randagent = random.choice(expanded_stats[prom])
        if randagent not in agents:
            logging.warning(
                "Non existing agent '%s' sampled for '%s' ignore and re-draw",
                randagent,
                agent,
            )
            to_fullfill.add(prom)
            continue
        res.append(randagent)
        for prov in agents[randagent]["provides"]:
            to_fullfill.discard(prov)

    return res


def expand_stats_list(stats: Dict[Text, Dict[Text, int]]) -> Dict[Text, List[Text]]:
    """Take the stats list and create lists of agents in the ratio of the stats count number,
    this is used in the montecarlo sampling by random.choice"""

    res = {}
    for prom, st in stats.items():
        exp = []
        for agent, count in st.items():
            exp += [agent] * count
        res[prom] = exp

    return res


def montecarlo(
    exp_stats: Dict[Text, List[Text]],
    agents: Dict[Text, Dict],
    base: Set[Text],
    stop_agents: Set[Text],
    seeds: Set[Text],
) -> Optional[Set[Text]]:
    """find possible new set of agents"""

    # import pdb

    # pdb.set_trace()
    # populate a set of requirements allready provided by the tecnique(s) in base
    allready_provides = seeds

    for agent in base:
        for prov in agents[agent]["provides"]:
            allready_provides.add(prov)

    res = set(base)

    while base:
        new_agent = set()
        for agent in base:
            sample = sample_agent(agent, agents, exp_stats, allready_provides)

            for agent in sample:
                allready_provides.update(agents[agent]["provides"])

            new_agent.update(sample)

        res.update(new_agent)

        for agent in new_agent:
            allready_provides.update(agents[agent]["provides"])

        all_requirements_provided = True
        for agent in res:
            if not set(agents[agent]["requires"]).issubset(allready_provides):
                all_requirements_provided = False

        if all_requirements_provided:
            for agent in res:
                if agent in stop_agents:
                    return res

        if not new_agent:
            for agent in res:
                for req in agents[agent]["requires"]:
                    if req not in allready_provides:
                        missing_counter[req] += 1
            return None

        base = new_agent

    return None  # Can't get here, the conditional returns are in the while loop above.


def validates(
    seeds: List[Text],
    agent_bundle: List[Text],
    agents: Dict,
    system_conditions: List[Text],
) -> bool:
    """check if the simulation is valid"""

    if not agent_bundle:
        return False

    sim = simulate(seeds, agent_bundle, agents, system_conditions)
    if sim.backburner:
        return False

    return True


def aggregate(agents: dict, strategy: str, data: Counter) -> Counter:
    """aggregate a result based on a strategy"""

    if not strategy:
        return data

    strategies = {
        "children": provreq.mcmc.aggregators.children.aggregate,
        "equivalence": provreq.mcmc.aggregators.equivalence.aggregate,
    }

    if strategy not in strategies:
        raise ValueError(f"Unknown aggregation strategy: {strategy}")

    return strategies[strategy](agents, data)  # type: ignore


def main() -> None:
    """main entry point"""

    args = command_line_arguments()

    if os.path.isabs(args.stats):
        stats_path = args.stats
    else:
        stats_path = os.path.join(args.data_dir, args.stats)

    with open(stats_path, encoding="utf8") as file_handle:
        stats = json.load(file_handle)

        agents, _, _ = config.read_agent_promises(args)

        if args.stop_agents:
            stop_agents = args.stop_agents
        elif args.stop_agent_class:
            stop_agents = {
                agent
                for agent, data in agents.items()
                if args.stop_agent_class in data["agent_class"]
            }
        else:
            stop_agents = {
                agent
                for agent, data in agents.items()
                if "Initial Access" in data["agent_class"]
            }

        if args.pre_seed_stop_agent_requirements:
            for agent in stop_agents:
                print(
                    f"Adding {agents[agent]['requires']} to the pre seeding due to stop agent {agent}"
                )
                args.seeds += agents[agent]["requires"]
            args.seeds = list(set(args.seeds))

        if args.seed_class:
            seed_agents = []
            for tid, agent in agents.items():
                if any(
                    seed_class in agent["agent_class"] for seed_class in args.seed_class
                ):
                    seed_agents += agent["provides"]
            print(
                (
                    f"Pre-seeding with {set(seed_agents)} from {', '.join(args.seed_class)} "
                    f"agent class{'es' if len(args.seed_class) > 1 else ''}."
                )
            )
            args.seeds = list(set(args.seeds + seed_agents))

        ignore_choke = stop_agents.union(set(args.agents))

        if not stop_agents:
            sys.stderr.write("Stop agents can not be empty!\n")
            sys.exit(1)

        c: Counter = Counter()

        exp_stats = expand_stats_list(stats)
        i = 0
        n = args.runs

        for seed in args.seeds:
            for k in agents:
                if seed in agents[k]["provides"]:
                    if args.hints:
                        print(
                            f"You could use {k} {agents[k]['name']} in place of {seed}"
                        )

        start = datetime.datetime.now()
        pbar = ProgressBar("Simulating", n)

        while i < n:
            sim = montecarlo(
                exp_stats, agents, set(args.agents), stop_agents, set(args.seeds)
            )
            if sim:
                sim.update(args.agents)
                # If it is allready stored, it is also allready validated.
                if c[frozenset(sim)] > 0 or validates(
                    args.seeds, list(sim), agents, []
                ):
                    c[frozenset(sim)] += 1
                    i += 1
                    pbar.update(i)

        stop = datetime.datetime.now()
        delta = stop - start
        pbar.done(f"done in {delta}")

        print(
            "Simulations ending due to missing requirements.. (stats for runs that did not complete)"
        )
        print(
            tabulate.tabulate(
                missing_counter.items(),
                headers=["promise", "count"],
                tablefmt="fancy_grid",
            )
        )

        print("Top choke points")
        print(
            tabulate.tabulate(
                find_choke_points(c, agents, ignore_choke).most_common(5),
                headers=["Agent", "Count"],
                tablefmt="fancy_grid",
            )
        )

        c = aggregate(agents, args.aggregation, c)

        print(f"Total number of potensial 'paths': {len(c)}")
        print(f"Top {args.top}")
        for res in c.most_common(args.top):
            print(f"{round(res[1] / n * 10000) / 100}% (n={res[1]})")
            sim = simulate(args.seeds, set(res[0]), agents, [])

            print(
                tabulate.tabulate(
                    stages_table(sim, agents, True, True),
                    headers="keys",
                    tablefmt="fancy_grid",
                )
            )

            print("---")


def find_choke_points(sims: Counter, agents: Dict, ignore: Set) -> Counter:
    """Find choke points in simulation"""

    c: Counter = Counter()
    for sim, n in sims.items():
        for agent in sim:
            if agent.startswith("T") and agent not in ignore:
                c[f"{agent}: {agents[agent]['name']}"] += 1

    return c
