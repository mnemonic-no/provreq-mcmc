"""Abstract reader to support reading agents from different sources"""

from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Text


class DataReader(ABC):
    """Abstract reader class to support reading agents from different sources"""

    @abstractmethod
    def iterate(self, filename: Text) -> Iterator[Dict[Text, List[Text]]]:
        """return an iterator returning a dictionary of bundles of MITRE agent IDS'"""

    def read(self, filename: Text) -> List[Dict[Text, List[Text]]]:
        """read a file returning a list dictionaries of bundles of agent IDs'"""

        return list(self.iterate(filename))
