# -*- coding: utf-8 -*-
"""helpful utils"""

import enum


class Units(enum.IntEnum):
    """ An enum for common binary units """
    KiB: 2 ** 10
    MiB: 2 ** 20
    GiB: 2 ** 30
    TiB: 2 ** 40

    @staticmethod
    def of(num: int) -> (int, "Units"):
        """ Converts an integer to use the largest unit possible.

        Args:
            num:

        Returns:
            A tuple of (Amount, unit).
        """
        for unit_name in reversed(Units.__members__):
            unit = Units[unit_name]
            if unit > num:
                continue
            return num / unit, unit
