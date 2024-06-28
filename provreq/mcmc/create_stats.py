import argparse
import json
import sys
from collections import defaultdict

from provreq.tools import config

from provreq.mcmc.mappings.mitre import remap
from provreq.mcmc.reader.aepdatareader import AEPDataReader
from provreq.mcmc.reader.datareader import DataReader
from provreq.mcmc.reader.defirdatareader import DEFIRDataReader
from provreq.mcmc.reader.mitresightingsreader import MITRESightingsReader
from provreq.mcmc.reader.u42datareader import U42PlaybookDataReader


def command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments"""

    parser = config.common_args("AEP Cyberhunt Requirements backsolver stats creator")

    parser.add_argument(
        "--defir-data", type=str, help="Files to generate probabilities"
    )

    parser.add_argument("--aep-data", type=str, help="Files to generate probabilities")

    parser.add_argument(
        "--u42-data",
        type=str,
        help="U42 Playbook repo zip to generate probabilities."
        + " Supports uri "
        + "(e.g https://github.com/pan-unit42/playbook_viewer/archive/master.zip)"
        + " and local file",
    )

    parser.add_argument(
        "--mitresightingsdump",
        type=str,
        help="MITRE Sightings dump file",
    )

    parser.add_argument(
        "--print-defir",
        default=False,
        action="store_true",
        help="Print parsed defir data",
    )

    parser.add_argument(
        "--skip-unused-agents",
        default=False,
        action="store_true",
        help="Do not include agents that has no purpose (eg. no provides is required by another agent)",
    )

    parser.add_argument(
        "--focus",
        type=str,
        default="require",
        help="Focus on require or provide. If provide, all provides by agents in "
        "bundle is added. Of require, only requirements is added",
    )

    parser.add_argument(
        "-o", "--output", type=str, default="stats.json", help="Store output"
    )

    args: argparse.Namespace = config.handle_args(parser, "generate")

    return args


def main() -> None:
    """main entry point"""

    args = command_line_arguments()

    if not (args.defir_data or args.aep_data or args.u42_data):
        sys.stderr.write("missing provreq-, u42- and/or defir- data\n")
        sys.exit(1)

    data = []
    if args.defir_data:
        print("Reading DEFIR")
        reader: DataReader = DEFIRDataReader()
        data += reader.read(args.defir_data)
    if args.aep_data:
        print("Reading AEP")
        reader = AEPDataReader()
        data += reader.read(args.aep_data)
    if args.u42_data:
        reader = U42PlaybookDataReader()
        data += reader.read(args.u42_data)
    if args.mitresightingsdump:
        reader = MITRESightingsReader()
        data += reader.read(args.mitresightingsdump)

    agents, _, _ = config.read_agent_promises(args)

    if args.focus not in ["require", "provide"]:
        print("Focus must be either require or provide")
        sys.exit(1)

    output: dict = {}
    # reqset: set = set()
    missing = set()
    if args.focus == "require":
        for bundle in data:
            print(bundle)
            for _, tech_list in bundle.items():
                list_reqs = set()
                for tech in tech_list:
                    tech = remap.get(tech, tech)
                    if not tech:
                        continue
                    if tech not in agents:
                        missing.add(tech)
                        continue
                    for req in agents[tech]["requires"]:
                        list_reqs.add(req)

                for pos_tech in tech_list:
                    pos_tech = remap.get(pos_tech, pos_tech)
                    if not pos_tech:
                        continue
                    if pos_tech not in agents:
                        missing.add(pos_tech)
                        continue
                    for req in list_reqs:
                        if req in agents[pos_tech]["provides"]:
                            if req not in output:
                                output[req] = defaultdict(int)
                            output[req][pos_tech] += 1

        if args.print_defir:
            from pprint import pprint

            pprint(data)
            for req in output:
                print(f"requirement: {req} provided by:")
                for tech, count in output[req].items():
                    print(f"\t{tech}: [{agents[tech]['name']}] : {count} times")
                print("--")
            sys.exit()

    with open(args.output, "w", encoding="utf-8") as f:
        sys.stderr.write("writing %s\n" % args.output)
        f.write(json.dumps(output))
    # if args.focus == "provide":
    # for tech_list in data.values():
    # for tech in tech_list:


if __name__ == "__main__":
    main()
