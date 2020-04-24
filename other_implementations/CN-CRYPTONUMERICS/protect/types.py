#!/usr/bin/env python3
# coding=utf8

from collections import defaultdict
from enum import Enum, auto
from functools import partial

import numpy as np


class DataType(Enum):
    STRING = auto()
    DATE = auto()
    INTEGER = auto()
    DECIMAL = auto()


# XXX: Add Date support
_data_type_compat = defaultdict(tuple, {
    DataType.STRING: (np.object, np.floating, np.integer),
    DataType.INTEGER: (np.integer,),
    DataType.DECIMAL: (np.floating, np.integer)
    })


def is_dtype_compat(our_type, dtype):
    try:
        dtype = dtype.type
    except AttributeError:
        pass
    return any(issubclass(dtype, t) for t in _data_type_compat[our_type])


def get_default_dtype(dtype):
    try:
        dtype = dtype.type
    except AttributeError:
        pass
    if issubclass(dtype, np.floating):
        return DataType.DECIMAL
    elif issubclass(dtype, np.integer):
        return DataType.INTEGER
    return DataType.STRING


class KindedType(Enum):
    AGE = auto()
    NAME = auto()
    EMAIL = auto()
    ADDRESS = auto()
    STATE = auto()
    CITY = auto()
    PROVINCE = auto()
    POSTCODE = auto()
    COUNTRY = auto()
    LATLONG = auto()
    GENDER = auto()
    DATE = auto()
    URL = auto()
    CREDITCARD = auto()
    PHONENUM = auto()


_kind_data_compat = defaultdict(partial(tuple, (DataType.STRING,)), {
    KindedType.AGE: (DataType.INTEGER, DataType.DECIMAL),
})


class IdType(Enum):
    IDENTIFYING = 'IDENTIFYING_ATTRIBUTE'
    SENSITIVE = 'SENSITIVE_ATTRIBUTE'
    INSENSITIVE = 'INSENSITIVE_ATTRIBUTE'
    QUASI = 'QUASI_IDENTIFYING_ATTRIBUTE'


class HierarchyBuilder(Enum):
    pass


_hierarchy_type_compat = {}
_default_kind_hierarchy = {}
