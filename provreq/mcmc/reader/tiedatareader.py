"""TIE data reader

https://raw.githubusercontent.com/center-for-threat-informed-defense/technique-inference-engine/refs/heads/main/data/combined_dataset_full_frequency.json
"""

import json
from typing import Dict, Iterator, List, Text

import provreq.mcmc.reader.datareader as datareader


class TIEDataReader(datareader.DataReader):
    """Read a TIE JSON file of reports with techniques"""

    def iterate(self, filename: Text) -> Iterator[Dict[Text, List[Text]]]:
        """Iterate over a DEFIR data set"""

        with open(filename, encoding="utf-8") as file_handle:
            data = json.load(file_handle)

            yield from (
                {report["id"]: report["mitre_techniques"]} for report in data["reports"]
            )
