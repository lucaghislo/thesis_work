#!/usr/bin/env python3
# coding=utf8

from enum import Enum

import pandas as pd


class Accessor(object):
    _ignore_attrs = (
        '_orig_dict',
        '_transform',
        '_validator',
        '_validate',
        '_callback',
        '_readonly'
        )

    def __init__(self, orig_dict, read_only=False,
                 transform=lambda x: x,
                 validator=lambda x, y: (True, None),
                 callback=lambda x, y: None):
        self._orig_dict = orig_dict
        self._transform = transform
        self._validator = validator
        self._callback = callback
        self._readonly = bool(read_only)

    def _validate(self, item, value):
        ok, msg = self._validator(item, value)

        if not ok:
            raise ValueError(f'Could not set {value}: {msg}')

    def __getattr__(self, attr):
        if attr not in Accessor._ignore_attrs:
            return self.__getitem__(attr)
        else:
            raise AttributeError(f'No attribute named {attr}')

    def __setattr__(self, attr, value):
        if attr not in Accessor._ignore_attrs:
            self.__setitem__(attr, value)
        else:
            object.__setattr__(self, attr, value)

    def __getitem__(self, item):
        if item not in self._orig_dict:
            raise ValueError(f'Unknown entry: {item}')
        value = self._orig_dict[item]
        if isinstance(value, Enum):
            return value.name
        return value

    def __setitem__(self, item, value):
        if self._readonly:
            raise ValueError('Cannot modify object')

        if item not in self._orig_dict:
            raise ValueError(f'Unknown entry: {item}')
        try:
            new_val = self._transform(value)
            self._validate(item, new_val)
            self._orig_dict[item] = new_val
            self._callback(item, new_val)
        except KeyError:
            raise ValueError(f'Unknown type: {value}')

    def __str__(self):
        return str({k:
                    v.name if isinstance(v, Enum)
                    else v
                    for k, v in self._orig_dict.items()})

    def __repr__(self):
        contents = [(k, v.name if isinstance(v, Enum) else v)
                    for k, v in self._orig_dict.items()]
        return repr(pd.Series([c[1] for c in contents],
                              index=[c[0] for c in contents]))
        # return repr()
