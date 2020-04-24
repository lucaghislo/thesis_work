#!/usr/bin/env python3
# coding=utf8

import re

from functools import lru_cache

from .types import DataType, IdType, KindedType, get_default_dtype

import numpy as np

from pandas.core.dtypes.dtypes import DatetimeTZDtype

import pycountry
import validators


_separators = '_\\- '
def _make_col_name_regexp(col_name):  # noqa: E302
    prefix = f'^(.*[${_separators}])*'
    suffix = f'\\d*([${_separators}].*)*$'
    return re.compile(f'{prefix}{col_name}{suffix}', re.I)


_id_frac_override = 1.0
_min_id_frac = 0.8
_min_match_frac = 0.9
_id_col_regexp = _make_col_name_regexp('id(ent(ifier)?)?')
_qid_col_regexp = _make_col_name_regexp('(seg(ment)?|demo(graphic)?)')
_id_kinds = (KindedType.CREDITCARD, KindedType.NAME, KindedType.PHONENUM,
             KindedType.EMAIL, KindedType.ADDRESS)
_qid_kinds = (KindedType.LATLONG, KindedType.AGE, KindedType.GENDER,
              KindedType.POSTCODE, KindedType.PROVINCE, KindedType.CITY,
              KindedType.STATE, KindedType.COUNTRY)
_col_name_regexps = {
    KindedType.NAME: _make_col_name_regexp('(first|last)?name'),
    KindedType.EMAIL: _make_col_name_regexp('email'),
    KindedType.ADDRESS: _make_col_name_regexp('address'),
    KindedType.STATE: _make_col_name_regexp('state'),
    KindedType.CITY: _make_col_name_regexp('city'),
    KindedType.PROVINCE: _make_col_name_regexp('prov(ince)?'),
    KindedType.POSTCODE: _make_col_name_regexp('[a-z1-9]*(zip|post)(code)?'
                                               '[a-z1-9]*'),
    KindedType.COUNTRY: _make_col_name_regexp('(country|nation(ality)?)'),
    KindedType.LATLONG: _make_col_name_regexp('(lat|long)(itude)?'),
    KindedType.GENDER: _make_col_name_regexp('[a-z1-9]*(gender|sex)[a-z1-9]*'),
    KindedType.AGE: _make_col_name_regexp('age'),
    KindedType.DATE: _make_col_name_regexp('(date|period|dt)'),
    KindedType.URL: _make_col_name_regexp('url'),
    KindedType.CREDITCARD: _make_col_name_regexp('credit'),
    KindedType.PHONENUM: _make_col_name_regexp(f'(phone)?[{_separators}]*'
                                               '(number)?')
    }


class TypeDetect(object):
    def __init__(self, col_name, col):
        self.col_name = col_name
        self.col = col
        self.unique_frac = (len(self.col.unique())
                            / self.col.count())

        self._itype = None
        self._ktype = None
        self._dtype = None

    @lru_cache()
    def get_itype(self):
        ktype = self.get_ktype()
        if (self.unique_frac >= _id_frac_override
            or (self.unique_frac >= _min_id_frac
                and _id_col_regexp.match(self.col_name))
            or (ktype in _id_kinds)):
            return IdType.IDENTIFYING
        elif ktype in _qid_kinds or _qid_col_regexp.match(self.col_name):
            return IdType.QUASI
        else:
            return IdType.INSENSITIVE

    @lru_cache()
    def get_ktype(self):
        maybe_types = {}

        if type(self.col.dtype) in (DatetimeTZDtype, np.datetime64):
            return KindedType.DATE
        elif any(isinstance(self.col.dtype, t)
                 for t in (np.float, np.integer)):
            # Check for number-ish types
            # Maybe: age, gender, creditcard, phone
            maybe_types[KindedType.AGE] = self._prob_age()
        elif self.col.dtype == np.object:
            # Check for string-ish types

            # First short-circuit more definitive types
            if self._is_email():
                return KindedType.EMAIL
            elif self._is_url():
                return KindedType.URL

            # Maybe: country, gender, postcode, phone
            maybe_types[KindedType.COUNTRY] = self._prob_country()
            maybe_types[KindedType.GENDER] = self._prob_gender()

        # XXX: Categorical?
        return self._resolve_ktype(maybe_types)

    @lru_cache()
    def get_dtype(self):
        return get_default_dtype(self.col.dtype)

    def get_types(self):
        return self.get_dtype(), self.get_itype(), self.get_ktype()

    def _is_email(self):
        pass

    def _is_url(self):
        pass

    _gender_regexp = re.compile('^(m(ale)?|f(emale)?)$', re.I)
    def _prob_gender(self):  # noqa: E301
        try:
            uniques = self.col.apply(lambda x: x.lower()).unique()
            if len(uniques) == 2 and all(TypeDetect._gender_regexp.match(v)
                                         for v in uniques):
                return _min_match_frac  # Always need a column name match
        except Exception:
            pass

        uniques = self.col.dropna().unique()

        if (len(uniques) == 2
            and ((uniques.min() == 0 and uniques.max() == 1)
                 or (uniques.min() == 1 and uniques.max() == 2))):
            return min(
                self.col.count() / len(self.col),
                _min_match_frac)  # Always need a column name match
        return 0.0

    def _prob_postcode(self):
        return 0.0

    def _prob_country(self):
        lengths = self.col.apply(lambda x: len(x)
                                 if isinstance(x, str)
                                 else None)
        return 0

    def _prob_age(self):
        return 0.0

    def _prob_credit_card(self):
        return 0.0

    def _prob_phone_number(self):
        return 0.0

    def _resolve_ktype(self, matches):
        for ktype, prob in sorted(matches.items(), key=lambda i: i[1]):
            if (prob >= 1.0
                or (prob >= _min_match_frac
                    and self._ktype_matches_col_name(ktype))):
                return ktype

    def _ktype_matches_col_name(self, ktype):
        return bool(_col_name_regexps[ktype].match(self.col_name))
