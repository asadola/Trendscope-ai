from abc import ABC, abstractmethod
from typing import List
from app.models.raw_event import RawEvent


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self) -> List[RawEvent]:
        """
        Extract raw events from a data source.
        Must return UNMODIFIED data.
        """
        pass
