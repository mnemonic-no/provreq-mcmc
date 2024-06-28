"""DFIR data reader"""

import csv
import json
from typing import Dict, Iterator, List, Text

import provreq.mcmc.reader.datareader as datareader


def _agents_from_element(element):
    """Extract agents from json elements"""

    incident = element["incident_name"]
    agents = element["agents"]
    agents = json.loads(agents.replace("'", '"'))

    techIDs = [tech.rsplit(" ", 1)[1] for tech in agents]

    return {incident: techIDs}


class DEFIRDataReader(datareader.DataReader):
    """Read a DFIR csv file of campaigns with agents"""

    def iterate(self, filename: Text) -> Iterator[Dict[Text, List[Text]]]:
        """Iterate over a DEFIR data set"""

        with open(filename, encoding="utf-8") as file_handle:
            csv_reader = csv.DictReader(file_handle)

            yield from (_agents_from_element(element) for element in csv_reader)
