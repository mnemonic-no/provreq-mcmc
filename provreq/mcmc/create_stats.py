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
from provreq.mcmc.reader.tiedatareader import TIEDataReader
from provreq.mcmc.reader.u42datareader import U42PlaybookDataReader


def command_line_arguments() -> argparse.Namespace:
    """Parse the command line arguments"""

    parser = config.common_args("AEP Cyberhunt Requirements backsolver stats creator")

    parser.add_argument(
        "--defir-data", type=str, help="Files to generate probabilities"
    )

    parser.add_argument("--aep-data", type=str, help="Files to generate probabilities")

    parser.add_argument(
        "--tie-data",
        type=str,
        help="Technique Inference Engine (TIE) data file for probabilities",
    )
    parser.add_argument(
        "--u42-data",
        type=str,
        help=(
            "U42 Playbook repo zip to generate probabilities."
            " Supports uri "
            "(e.g https://github.com/pan-unit42/playbook_viewer/archive/master.zip)"
            " and local file"
        ),
    )

    parser.add_argument(
        "--mitresightingsdump",
        type=str,
        help="MITRE Sightings dump file",
    )

    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Turn on debug output",
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

    data: list = []
    if args.defir_data:
        print("Reading DEFIR")
        reader: DataReader = DEFIRDataReader()
        n = len(data)
        data += reader.read(args.defir_data)
        print(len(data) - n, "new entries")
    if args.tie_data:
        print("Reading TIE")
        reader = TIEDataReader()
        n = len(data)
        data += reader.read(args.tie_data)
        print(len(data) - n, "new entries")
    if args.aep_data:
        print("Reading AEP")
        reader = AEPDataReader()
        n = len(data)
        data += reader.read(args.aep_data)
        print(len(data) - n, "new entries")
    if args.u42_data:
        print("Reading u42 data")
        reader = U42PlaybookDataReader()
        n = len(data)
        data += reader.read(args.u42_data)
        print(len(data) - n, "new entries")
    if args.mitresightingsdump:
        print("Reading MITRESightings")
        reader = MITRESightingsReader()
        n = len(data)
        data += reader.read(args.mitresightingsdump)
        print(len(data) - n, "new entries")

    if args.debug:
        print("read agent promises", args.data_dir, args.agent_promises)

    agents, _, _ = config.read_agent_promises(args)

    if args.debug:
        print("done reading agent promises")

    if args.focus not in ["require", "provide"]:
        print("Focus must be either require or provide")
        sys.exit(1)

    output: dict = {}
    # reqset: set = set()
    missing = set()
    if args.focus == "require":
        for bundle in data:
            # print(bundle)
            if args.debug:
                print("bundle:", type(bundle))
            for _, agent_list in bundle.items():
                if args.debug:
                    print("Len agent_list", len(agent_list))
                list_reqs = set()

                for agent in agent_list:
                    agent = remap.get(agent, agent)
                    if not agent:
                        continue
                    if agent not in agents:
                        missing.add(agent)
                        if args.debug:
                            print("DEBUG: missing", agent)
                        continue
                    for req in agents[agent]["requires"]:
                        if args.debug:
                            print("Adding list_reqs", agent, req)
                        list_reqs.add(req)

                if args.debug:
                    print("len list_reqs", len(list_reqs))
                    print("len agent_list", len(agent_list))

                for pos_agent in agent_list:
                    pos_agent = remap.get(pos_agent, pos_agent)
                    if not pos_agent:
                        if args.debug:
                            print("Continue due to pos_agent", pos_agent)
                        continue
                    if pos_agent not in agents:
                        missing.add(pos_agent)
                        if args.debug:
                            print("Continue due missing pos_agent", pos_agent)
                        continue
                    for req in list_reqs:
                        if req in agents[pos_agent]["provides"]:
                            if req not in output:
                                output[req] = defaultdict(int)
                            if args.debug:
                                print(
                                    "Adding output for req, pos_agent", req, pos_agent
                                )
                            output[req][pos_agent] += 1

        if args.print_defir:
            from pprint import pprint

            pprint(data)
            for req in output:
                print(f"requirement: {req} provided by:")
                for agent, count in output[req].items():
                    print(f"\t{agent}: [{agents[agent]['name']}] : {count} times")
                print("--")
            sys.exit()

    with open(args.output, "w", encoding="utf-8") as f:
        sys.stderr.write("writing %s\n" % args.output)
        f.write(json.dumps(output))
    # if args.focus == "provide":
    # for agent_list in data.values():
    # for agent in agent_list:


if __name__ == "__main__":
    main()
