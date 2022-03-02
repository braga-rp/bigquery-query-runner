from typing import Sequence


class QueryResult:
    def __init__(self, file_path: str, sample: Sequence[str]):
        self._file_path = file_path
        self._sample = sample

    @property
    def file_path(self):
        return self._file_path

    @property
    def sample(self):
        return self._sample
