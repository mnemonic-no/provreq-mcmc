import io
import re
import zipfile
from pathlib import Path
from typing import IO, Callable, Dict, Iterator, List, Optional, Set, Tuple

import requests
import stix2.exceptions
from stix2 import parse
from stix2.v20.bundle import Bundle

from provreq.mcmc.reader import datareader


def file_zip(filename: str) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Open Zip File and yield (filename, file-like object) pairs
    """

    with zipfile.ZipFile(filename) as zipreader:
        for zipinfo in zipreader.infolist():
            with zipreader.open(zipinfo) as zf_handle:
                yield zipinfo.filename, zf_handle


def url_zip(url: str) -> Iterator[Tuple[str, IO[bytes]]]:
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url, timeout=30)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipreader:
        for zipinfo in zipreader.infolist():
            with zipreader.open(zipinfo) as zf_handle:
                yield zipinfo.filename, zf_handle


def playbook_agents(playbook: Bundle) -> Set[str]:
    """Return the agents referenced to a threat actor in the playbook"""

    agents: Set[str] = set()
    for obj in playbook.objects:
        if not hasattr(obj, "type"):
            print(f"Could not read object of type {obj['type']}")
            continue
        if obj.type == "attack-pattern":
            agents.update(
                {
                    ref.external_id
                    for ref in obj.external_references
                    if ref.source_name == "mitre-attack"
                }
            )
    return agents


def _get_reader(
    playbook_file: str,
) -> Callable[[str], Iterator[Tuple[str, IO[bytes]]]]:
    """figure out the correct reader based on the filename"""

    if playbook_file.startswith("http"):
        return url_zip
    return file_zip


def _extract_playbook_agents(file, filename) -> Optional[Dict[str, List[str]]]:
    """check if the filename conforms to a playbook file, if so extract the agents used"""

    print(f"Trying {filename}")
    if re.search(r"/playbook_json/.*.json$", filename):
        try:
            playbook = parse(file, allow_custom=True)
            print(f"Parsing {filename}")
        except stix2.exceptions.InvalidValueError as err:
            print(
                f"u42 reader: _extract_playbook_agents: Could not parse {filename} -> {err}"
            )
            return None

        agents = playbook_agents(playbook)
        return {Path(filename).name: list(agents)}
    return None


class U42PlaybookDataReader(datareader.DataReader):
    """Read a U42 Playbook file of campaigns with agents"""

    def iterate(self, filename: str) -> Iterator[Dict[str, List[str]]]:
        """Iterate over a playbooks' data set"""

        zip_reader = _get_reader(filename)

        for content_filename, file in zip_reader(filename):
            agents = _extract_playbook_agents(file, content_filename)
            if agents:
                yield agents
            else:
                print(f"Skipping {content_filename}, no return from parser")
