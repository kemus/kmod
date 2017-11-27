# -*- coding: utf-8 -*-
"""stuff"""
import typing

from type_play import optional

T = typing.TypeVar('T')


class Node(typing.Iterator[T]):
    """An node in the chunk."""

    def __init__(self, item: T,
                 prev: "Node"[T] = None,
                 next: "Node"[T] = None) -> None:
        self.prev = prev
        self.item = item
        self.next = next

    def __next__(self) -> _T_co:
        return self.next


class LinkedDict(typing.MutableMapping[[int], Node[T]]):
    """  python pls  """

    def __init__(self) -> None:
        self.__dict: typing.Dict[[int], Node[T]] = dict()
        self.__start: optional.Optional(Node[T]) = optional.Optional()
        self.__len: int = 0

    def __len__(self) -> int:
        return self.__len

    def __iter__(self) -> typing.Iterator[T]:
        pass

    def __setitem__(self, k: _KT, v: _VT) -> None:
        pass

    def __delitem__(self, v: _KT) -> None:
        pass

    def __getitem__(self, k: _KT) -> _VT_co:
        pass





class Chunk(typing.MutableSequence[T]):
    """ A sequence that can be missing items. """

    def __init__(self, sequence: typing.Sequence = None) -> None:
        """
        Args:
             sequence: optional, initializes the chunk with this sequence.
        """
        self.__chunk_dict: typing.Mapping[int, T] = dict()
        self.__start_node: Node = None
        self.__len: int = 0

        if sequence:
            self.overwrite(sequence)

    def __len__(self) -> int:
        pass

    def __setitem__(self, i: int, o: T) -> None:
        self.__chunk_dict[i] = o

    def __getitem__(self, i: int) -> T:
        return self.__chunk_dict[i]

    def __delitem__(self, i: int) -> None:
        del self.__chunk_dict[i]

    def overwrite(self, items: typing.Sequence[T], start: int = 0) -> None:
        """ Sets values in the Chunk. This overwrites existing values at the
        relevant indices.

        Args:
            items: values to set in the Chunk
            start: start setting values at this index
        """
        for i in range(len(items)):
            self.__setitem__(start + i, items[i])

    def _shift(self, index: int, amount: int):
        pass

    def insert(self, index: int, item: T) -> None:
        """ Insert one item into the chunk. This does not overwrite existing
        values, it shifts any values found to the right.
        Args:
            index: location to insert item
            item: item to insert.
        """

        pass

'''
class Cache(typing.Generic[T]):
    def __init__(self, func: typing.Callable[[int], T]) -> None:
        self.func = func
        self.__chunk: T = dict()
        self.__len: int = 0


class ChunkCache(typing.MutableMapping[str, CacheChunk]):
    """ A cache. """

    def __init__(self, chunk_size: int = 8 * utils.units.Units.KiB) -> None:
        self.chunk_size = chunk_size
        self.__cache = collections.defaultdict(str)

    def __len__(self) -> int:
        return len(self.__cache)

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.__cache)

    def __setitem__(self, k: str, v: typing.Sequence[str]) -> None:
        self.__cache[k] = v

    def __delitem__(self, k: str) -> None:
        del self.__cache[k]

    def __getitem__(self, k: str) -> typing.Sequence[str]:
        return self.__cache[k]'''
