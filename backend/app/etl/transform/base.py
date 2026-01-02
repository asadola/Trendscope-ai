from abc import ABC, abstractmethod
from app.models.raw_event import RawEvent
from app.models.clean_event import CleanEvent


class BaseTransformer(ABC):

    @abstractmethod
    def transform(self, event: RawEvent) -> CleanEvent:
        """
        Convert RawEvent → CleanEvent
        """
        pass
