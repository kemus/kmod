from utils.units import Units
import collections
from typing import Sequence, TypeVar, Dict, Mapping


class ChunkReader(object):
    def __init__(self, cache_limit: int = 0) -> None:
        self.__cache: Mapping[int, str] = {}
        self.cache_limit = cache_limit

    class __Reader(Sequence[str]):
        def __init__(self, file_path: str) -> None:
            self.file_path = file_path

        def __getitem__(self, index: int) -> str:
            pass

        def chunk_reader(self, filename, chunk_size=8 * 1024, max_size=None):
            """Generator that reads a file in chunks of bytes"""
            read = 0
            # Yield as much as possible from cache first
            while True:
                if max_size and read > max_size:
                    return
                if read < self.cache_limit and len(cache[filename]) > read:
                    chunk = cache[filename][read:read + chunk_size]
                    read += len(chunk)
                    yield chunk
                else:
                    break
            # Couldn't get more from cache, but still need more :(
            with open(filename, 'rb') as f:
                f.seek(read)
                while True:
                    if max_size and read > max_size:
                        return
                    chunk = f.read(chunk_size)
                    if not chunk:
                        return
                    # add to cache, avoid re-reading
                    if read < self.cache_limit:
                        cachunk = chunk[
                                  :min(self.cache_limit - read, chunk_size)]
                        cache[filename] += cachunk
                    read += len(chunk)
                    yield chunk

    def read(self, filename: str, chunk_size: int = 8*Units.KiB,
             max_size: int = None) -> Sequence[str]:
        """ Read a file, in chunks

        Args:
            filename:
            chunk_size:
            max_size:

        Returns:

        """
