from numbers import Number
from collections import defaultdict
from itertools import repeat
from fractions import Fraction


class WeightedSet:
    def __init__(self, weighted_items=None):
        self._weights = defaultdict(int)
        if weighted_items is not None:
            self.update(weighted_items)

    def __repr__(self):
        items = (
            "{"
            + ", ".join(["{} * {}".format(weight, item) for item, weight in self])
            + "}"
        )
        return "<{} {}>".format(self.__class__.__name__, items)

    def add(self, item, weight=1):
        self._weights[item] += Fraction(weight)

    def update(self, items):
        for item, weight in items:
            self.add(item, weight)

    @property
    def total_weight(self):
        return sum(self._weights.values())

    def __iter__(self):
        return iter(self._weights.items())

    def __eq__(self, other):
        return set(self) == set(other)

    def __imul__(self, multiplier):
        if not isinstance(multiplier, Number):
            raise NotImplementedError
        for item in self._weights:
            self._weights[item] *= multiplier
        return self

    def __mul__(self, multiplier):
        if not isinstance(multiplier, Number):
            raise NotImplementedError
        return self.__class__((item, weight * multiplier) for item, weight in self)

    def __rmul__(self, multiplier):
        return self.__mul__(multiplier)

    @classmethod
    def from_items(cls, items):
        return cls(zip(items, repeat(1)))
