"""
This module provides a basic implementation of a generic data structure
"""
from abc import ABC


class ADS(ABC):
    """
    A generic data structure
    """

    @property
    def get_id(self):
        """
        get_id
        """
        return "id"

    @property
    def ds_func(self):
        """
        simple way to get methods exposed
        """
        return {x for x in self.__class__.__dict__ if not str(x).startswith("_")}
