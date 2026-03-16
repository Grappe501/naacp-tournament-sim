from abc import ABC, abstractmethod
from typing import Any

class BaseSourceAdapter(ABC):
    source_name: str = "base"

    @abstractmethod
    def fetch(self, **kwargs) -> Any:
        raise NotImplementedError
