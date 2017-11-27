"""Optional"""
# -*- coding: utf-8 -*-
import typing

T = typing.TypeVar('T')


class EmptyOptionalError(LookupError):
    """ Raised when Optional.get is called on an empty Optional"""


class Optional(typing.Generic[T]):
    """ Optionally contains a value. """
    __empty: "Optional" = None

    def __new__(cls, value: T = None) -> "Optional":
        instance = super().__new__(cls, value)
        if value is None:
            if cls.__empty is None:
                cls.__empty = instance
            return cls.__empty
        return instance

    def __init__(self, value: T = None):
        self.__value = value

    def get(self, default: T = None) -> T:
        """ Gets the value in the optional.
        Args:
            default: (optional) value to return if the optional is empty.
        Returns:
            The value inside in the optional.
        Raises:
            EmptyOptionalError if the optional is empty and default is not set.
        """
        if self.__value is not None:
            return self.__value
        if default is not None:
            return default
        raise EmptyOptionalError

    R = typing.TypeVar('R')

    def map(self, func: typing.Callable[[T], R]) -> "Optional[R]":
        """ If the optional isn't empty, map the value to func(value).
        Args:
            func: The callable used to map the optional's value.

        Returns:
            Optional(func(value)) if the optional is not empty, otherwise
            returns an empty Optional,
        """
        if self.__value is None:
            return self
        else:
            return Optional(func(self.__value))

    def is_empty(self) -> bool:
        """
        Returns:
            True if the optional does not contain a value.
        """
        return self is not Optional()

    def __hash__(self) -> int:
        return hash((Optional.__class__, self.__value))

    def __eq__(self, other: "Optional") -> bool:
        return self.__value == other.__value


EMPTY = Optional()
