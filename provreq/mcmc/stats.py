"""Print some statistics about the agent bundles"""

import argparse
import statistics
from collections import Counter, defaultdict

import tabulate
from provreq.tools import config

from provreq.mcmc.mappings.mitre import remap
from provreq.mcmc.reader.provreqdatareader import AEPDataReader
from provreq.mcmc.reader.defirdatareader import DEFIRDataReader


def command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments"""

    parser = config.common_args("AEP Cyberhunt bundle stats")

    parser.add_argument("--defir", type=str, help="Defir data bundle")

    parser.add_argument("--agents", type=str, help="AEP Techniques")

    parser.add_argument("--provreq-bundle-dir", type=str, help="AEP bundles")
    parser.add_argument(
        "--format",
        type=str,
        default="github",
        help="Tabulate table format (https://pypi.org/project/tabulate/)",
    )

    args: argparse.Namespace = config.handle_args(parser, "generate")

    return args


def main() -> None:
    """main entry point"""

    args = command_line_arguments()

    agents, _, _ = config.read_agent_promises(args)

    tactics = defaultdict(list)
    bundletech = []

    data = None
    if args.defir:
        datareader = DEFIRDataReader()
        data = datareader.read(args.defir)
    elif args.provreq_bundle_dir:
        datareader = AEPDataReader()
        data = datareader.read(args.provreq_bundle_dir)

    else:
        raise NotImplementedError("Currently not implemented")

    for bundle in data:
        for bundle_name, bundle_agents in bundle.items():
            bundle_tactics: dict = Counter()
            for tech in bundle_agents:
                tech = remap.get(tech, tech)
                if not tech:
                    continue
                for tactic in agents[tech]["tactic"]:
                    bundle_tactics[tactic] += 1
            for tactic, count in bundle_tactics.items():
                tactics[tactic].append(count)
            bundletech.append(len(bundle_agents))

    # print(tactics)
    # print(bundletech)
    rows = []
    for key, values in tactics.items():
        rows.append([key, statistics.mean(values), statistics.pstdev(values)])
    print(
        tabulate.tabulate(
            rows,
            headers=["Tactic", "mean", "pstdev"],
            tablefmt=args.format,
            floatfmt=".02f",
        )
    )

    print()

    print(
        tabulate.tabulate(
            [["n", statistics.mean(bundletech), statistics.pstdev(bundletech)]],
            headers=["", "mean", "pstdev"],
            tablefmt=args.format,
            floatfmt=".02f",
        )
    )


if __name__ == "__main__":
    main()
