"""AEP data reader"""

import json
from glob import glob
from pathlib import Path
from typing import Dict, Iterator, List, Text

from provreq.mcmc.reader import datareader


class AEPDataReader(datareader.DataReader):
    """Read a DFIR csv file of campaigns with agents"""

    def iterate(self, filename: Text) -> Iterator[Dict[Text, List[Text]]]:
        """Iterate over a DEFIR data set"""

        for bundle_file in glob(f"{filename}/*"):
            with open(bundle_file, encoding="utf-8") as file_handle:
                data = json.load(file_handle)

                yield {Path(bundle_file).name: data.get("agents", [])}
