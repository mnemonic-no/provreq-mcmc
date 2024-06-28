"""MITRE Sightings data reader"""

import json
from glob import glob
from pathlib import Path
from typing import Dict, Iterator, List, Text

from provreq.mcmc.reader import datareader


class MITRESightingsReader(datareader.DataReader):
    """Read a MITRE Sightings dump csv file of sighted agents"""

    def iterate(self, filename: Text) -> Iterator[Dict[Text, List[Text]]]:
        """Iterate over a Sightings dump"""

        with open(filename, encoding="utf-8") as file_handle:
            data = json.load(file_handle)
            yield from ({sighting["id"]: sighting["tid"]} for sighting in data)
