# -*- coding: utf-8 -*-
""" Display the progress of your code. """

import datetime
import math
import sys


class ProgressBar(object):
    """ Used to display a text-based progress bar. """

    def __init__(self, name: str, total: int,
                 output_every: datetime.timedelta=datetime.timedelta.resolution,
                 precision: int=2) -> None:
        """
        Args:
            name:
            total: The total amount of work.
            output_every: Update the output at this often.
            precision: Show percentage to this precision.
        """
        now = datetime.datetime.now()
        self.name = name
        self.total = total
        self.output_every = output_every
        self.digits = math.ceil(math.log10(total))
        self.precision = precision
        self.start_time = now
        self.time = now
        self.processed = 0
        self.count = 0
        self.status = ''

        self._assert_valid_input()

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, exc_type: type, exc_val: object, exc_tb: object) -> None:
        self.progress(self.count, self.status, force_update=True)
        print()  # an _empty line

    def _assert_valid_input(self) -> None:
        assert self.total > 0
        assert self.output_every > datetime.timedelta.resolution
        assert self.precision >= 0

    def progress(self, count: int, status: str = None,
                 force_update: bool = False) -> None:
        """ Call to mark progress.

        Args:
            count: The amount of work completed.
            status: Optional
            force_update:

        Returns:

        """
        now = datetime.datetime.now()
        self.count = count
        self.status = status
        if not force_update and self.time + self.output_every > now:
            return

        speed = self.get_speed(now)
        eta = self.get_eta(speed)

        output = self.build_output(speed, eta)
        sys.stdout.write(output)
        sys.stdout.flush()

    def build_output(self, speed: float, eta: datetime.timedelta) -> str:
        """ Builds the string that will be output to show progress.
        Args:
            speed: Amount of work done per second.
            eta: Estimated time to complete the remaining work.

        Returns:
            The string to output to show progress
        """
        percent = round(100 * float(self.count) / self.total, self.precision)
        pad_right = '{:>{width}}'
        pad_decimals = '{.{precision}f}%'
        data = {
            'file_path': self.name,
            'count': pad_right.format(self.count, width=self.digits),
            'total': pad_right.format(self.total, width=self.digits),
            'percent': pad_decimals.format(percent, precision=self.precision),
            'speed': '{}/sec'.format(int(speed)),
            'eta': str(eta),
        }
        output = '{file_path}: {count}/{total} | {percent} | {speed} | {eta}' % data
        return output

    def get_speed(self, now: datetime.datetime) -> float:
        """ Get the progress speed. Safe against dividing by 0.
        Args:
            now: Datetime when self.progress was called.

        Returns:
            Average work done per second, or 0 if no work has been done yet.
        """
        if self.count <= 0:
            return 0
        if now == self.start_time:
            now += datetime.timedelta.resolution  # avoid dividing by 0.
        seconds = (now - self.start_time).total_seconds()
        return self.count / seconds

    def get_eta(self, speed: float) -> datetime.timedelta:
        """ Get time left, given how much work is done and the estimated speed.

        Args:
            speed: Average work done per second.

        Returns:
            An estimate for the time needed to finish the remaining work.
        """
        if speed <= 0:  # avoid dividing by 0
            return datetime.timedelta.max
        seconds_left = (self.total - self.count) / speed
        return datetime.timedelta(seconds=seconds_left)
