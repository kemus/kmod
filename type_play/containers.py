# -*- coding: utf-8 -*-
import abc
import typing

T = typing.TypeVar('T')
A = typing.TypeVar('A')
B = typing.TypeVar('B')

Comparator = typing.Callable[[typing.Generic[A], typing.Generic[B]], bool]


class Relation(typing.Generic[A], typing.Generic[B], abc.ABC):
    @property
    @abc.abstractmethod
    def get_comparator(self) -> Comparator:
        pass

    def compare(self, a: A, b: B) -> bool:
        return self.get_comparator()(a, b)


class Equality(Relation[A, B]):
    @property
    def get_comparator(self) -> Comparator[A, B]:
        return lambda a, b: a == b


class Container(typing.Generic[T], abc.ABC):
    @abc.abstractmethod
    def contains(self, item: T) -> object:
        pass


class Ordered(typing.Generic[T], abc.ABC):
    pass


class Hashable(typing.Generic[T], abc.ABC):
    def hash(self) -> Hash:
        pass
