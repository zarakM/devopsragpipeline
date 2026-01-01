from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, file_path: str, content: str) -> List[Dict[str, Any]]:
        """
        Parses content and returns a list of chunks with metadata.
        Each chunk should have:
        - content: str
        - metadata: dict
        """
        pass
