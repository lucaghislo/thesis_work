#!/usr/bin/env python3
# coding=utf8

import json

from functools import partial
from io import StringIO, BytesIO

import pandas as pd

from jnius import JavaException

from .accessor import Accessor
from .types import (DataType, IdType, KindedType,
                    is_dtype_compat, _kind_data_compat,
                    get_default_dtype)
from .detect import TypeDetect
from .hierarchy import Hierarchy, DataHierarchy
from .java import (Protect as JavaProtect, ProtectConfig, ByteArrayInputStream,
                   HashMap)
from .privacy import KAnonymity, GlobalPrivacyModel, AttributePrivacyModel
from .quality import Loss


def _valid_data_type(df, item, value):
    df_dtype = getattr(df.dtypes, item)
    ok = is_dtype_compat(value, df_dtype)

    if ok:
        return True, None
    return False, (f'Column {item} has type {df_dtype} which is not '
                   f'compatible with {value.name}')


def _set_data_type_callback(kind_types, item, value):
    if item not in kind_types:
        return
    kind = kind_types[item]
    if value not in _kind_data_compat[kind]:
        kind_types[item] = None


def _valid_kinded_type(data_types, item, value):
    data_type = data_types[item]
    ok = data_type in _kind_data_compat[value]

    if ok:
        return True, None
    return False, f'Kind {value} is not valid for type {data_type.name}'


def _valid_hierarchy():
    pass


def _set_id_type_callback(hierarchies, item, value):
    if value != IdType.QUASI and item in hierarchies:
        hierarchies[item] = None


def _validate_hierarchy(df, item, value):
    if value is not None and not isinstance(value, Hierarchy):
        return False, f'Value {value} is not a hierarchy'
    try:
        if value is not None:
            value._validate(df, item)
    except ValueError as ve:
        return False, ve.message
    return True, None


def _set_hierarchy_callback(id_types, item, value):
    id_types[item] = IdType.QUASI


_default_hierarchies = {}


class Protect(object):
    '''Main interface to CryptoNumerics's Privacy Protection.

    Operates on Pandas DataFrames, returning new privacy-protected
    DataFrames.

    Parameters
    ----------
    df : Pandas DataFrame
        The input dataset, as a Pandas DataFrame.
    privacy_model : :class:`~cn.protect.privacy.PrivacyModel`\\.
        A privacy model from the :mod:`~cn.protect.privacy` module. Defaults
        to :class:`~cn.protect.privacy.KAnonymity`\\(3).
    quality_model : :class:`~cn.protect.quality.QualityModel`\\.
        A quality model from the :mod:`~cn.protect.quality` module. Defaults
        to :class:`~cn.protect.quality.Loss`\\.
    suppression : float
        A floating point value between [0.0, 1.0] which represents the maximum
        fraction of rows which can be suppressed. Defaults to 0.0.
    infer_types : bool
        Whether or not to infer some additional type information from the
        DataFrame. Note that data types are dependent on the types specified
        in the DataFrame regardless. Defaults to ``True``.
    use_default_hierarchies : bool
        Whether or not to add certain hierarchies based on a heuristic applied
        to the DataFrame. Defaults to ``True``.

    '''

    def __init__(self, df, privacy_model=None, quality_model=None,
                 suppression=0.0, infer_types=True, heuristic_step_limit=200,
                 use_default_hierarchies=True):
        self.df = df

        if privacy_model is None:
            self.privacy_model = KAnonymity(3)
        elif not isinstance(privacy_model, GlobalPrivacyModel):
            raise TypeError('Must supply a global privacy model')
        else:
            self.privacy_model = privacy_model

        self.quality_model = quality_model if quality_model else Loss()

        self.suppression = suppression
        self.heuristic_step_limit = heuristic_step_limit
        self.heuristic_search = False

        self.info_loss = None
        self.transformation = None
        self._stats = {}

        self._data_types = {}
        self._kinded_types = {}
        self._id_types = {}
        self._hierarchies = {}
        self._col_privacy_models = {}

        for col in df:
            if infer_types:
                data_type, id_type, kinded_type = TypeDetect(
                    col, self.df[col]).get_types()
                self._hierarchies[col] = _default_hierarchies.get(
                    kinded_type)
            else:
                data_type = get_default_dtype(self.df[col].dtype)
                id_type = IdType.INSENSITIVE
                kinded_type = None
                self._hierarchies[col] = None

            self._data_types[col] = data_type
            self._id_types[col] = id_type
            self._kinded_types[col] = kinded_type
            self._hierarchies[col] = None
            self._col_privacy_models[col] = None

    def protect(self):
        '''Apply the privacy protection as specified, returning a DataFrame.

        Returns
        -------
        Pandas DataFrame
            A privacy-protected version of ``df``, after applying
            the specified protection parameters.
        '''
        self._validate_types()

        # XXX: Check for at least one QI

        with StringIO() as buf:
            self.df.to_csv(buf, index=False)
            contents = buf.getvalue().encode('utf-8')

        try:
            config_from = getattr(ProtectConfig, 'from')
            config = config_from(json.dumps(self._gen_config()))
        except JavaException:
            raise RuntimeError('Could not construct configuration.')

        try:
            data_hier = HashMap()
            for col, hier in self._hierarchies.items():
                if not isinstance(hier, DataHierarchy):
                    continue

                with StringIO() as buf:
                    hier.df.to_csv(buf, index=False, header=False)
                    hier_contents = buf.getvalue().encode('utf-8')
                data_hier.put(col, ByteArrayInputStream(hier_contents))
        except JavaException:
            raise RuntimeError('Could not serialize data frame.')

        try:
            prot = JavaProtect(config, ByteArrayInputStream(contents),
                               data_hier)
            prot.anonymize()
        except JavaException as je:
            classname = je.classname.rsplit('.', 1)[-1]
            if (classname == 'NoTransformationAppliedException'):
                raise RuntimeError('Constraints satisfied, but no '
                                   'transformation necessary.')
            raise RuntimeError('Error finding solution.')

        try:
            self.info_loss = prot.getInformationLoss()
            self.transformation = prot.getTransformation()
        except JavaException:
            raise RuntimeError('Failed to fetch solution metadata')

        try:
            prot.analyze()
            stats = json.loads(prot.getStatisticsJson())
            self._stats = {**stats['anonymizationStatistics'],
                           **stats['generalStatistics']}
        except JavaException:
            raise RuntimeError('Failed to fetch statistics')

        try:
            with BytesIO(prot.getOutput().readAllBytes().tostring()) as buf:
                return pd.read_csv(buf)
        except JavaException:
            raise RuntimeError('Could not deserialize results.')

    def add_privacy_model(self, col, privacy_model):
        '''Adds an attribute privacy model for sensitive attributes to the
        specified column.
        '''
        if col not in self.df:
            raise ValueError('Must supply privacy model for an existing '
                             'column')
        elif not isinstance(privacy_model, AttributePrivacyModel):
            raise TypeError('Must supply a column privacy model')
        self._col_privacy_models[col] = privacy_model

    @property
    def stats(self):
        return Accessor(self._stats, read_only=True)

    @property
    def suppression(self):
        '''A floating point value between [0.0, 1.0] which represents the maximum
        fraction of rows which can be
        :ref:`suppressed <transform_suppression>`.

        Can be used to read the current value:
            >>> prot.suppression
            0.0

        or to set a new limit:
            >>> prot.suppression = 0.2
        '''
        return self._suppression

    @suppression.setter
    def suppression(self, suppression):
        try:
            _suppression = float(suppression)
            if _suppression < 0 or _suppression > 1:
                raise ValueError
        except ValueError:
            raise ValueError('Suppression must be a floating point number '
                             'between 0 and 1.')
        self._suppression = _suppression

    @property
    def heuristic_step_limit(self):
        return self._heuristic_step_limit

    @heuristic_step_limit.setter
    def heuristic_step_limit(self, heuristic_step_limit):
        try:
            _heuristic_step_limit = int(heuristic_step_limit)
            if _heuristic_step_limit < 0 or _heuristic_step_limit > 10000:
                raise ValueError
        except ValueError:
            raise ValueError('heuristic_step_limit must be an integer '
                             'between 0 and 10000.')
        self._heuristic_step_limit = _heuristic_step_limit

    @property
    def heuristic_search(self):
        return self._heuristic_search

    @heuristic_search.setter
    def heuristic_search(self, heuristic_search):
        try:
            _heuristic_search = bool(heuristic_search)
        except ValueError:
            raise ValueError('heuristic_step_limit must be an integer '
                             'between 0 and 10000.')
        self._heuristic_search = _heuristic_search

    @property
    def dtypes(self):
        '''The *data types* associated with each attribute.

        These are used in combination with the Hierarchies in order to
        define the transformations applied to the data. They are
        always inferred from the input DataFrame to ensure that only
        valid operations are applied to the data.

        The possible values, specified as case-insensitive strings, are:

        * string
        * decimal
        * integer

        These *dtypes* can be read via the dtypes property:
            >>> prot.dtypes
            PassengerId    INTEGER
            Survived       INTEGER
            Pclass         INTEGER
            Name            STRING
            Sex             STRING
            Age            DECIMAL
            SibSp          INTEGER
            Parch          INTEGER
            Ticket          STRING
            Fare           DECIMAL
            Cabin           STRING
            Embarked        STRING
            dtype: object

        And be read or set via either the indexing operator:
            >>> prot.dtypes['Fare']
            'STRING'
            >>> prot.dtypes['Fare'] = 'decimal'

        or via property access:
            >>> prot.dtypes.Fare
            'DECIMAL'
            >>> prot.dtypes.Fare = 'string'
        '''
        return Accessor(self._data_types,
                        transform=lambda val: DataType[val.upper()],
                        validator=partial(_valid_data_type, self.df),
                        callback=partial(_set_data_type_callback,
                                         self._kinded_types))

    @property
    def ktypes(self):
        '''The *kinded types* associated with each attribute.

        These *ktypes* are used for inference of settings, notably
        *itypes* and *hierarchies*. They are completely optional, and
        can be ignored if desired.

        '''
        return Accessor(self._kinded_types,
                        transform=lambda val: KindedType[val.upper()],
                        validator=partial(_valid_kinded_type,
                                          self._data_types))

    @property
    def itypes(self):
        '''The :ref:`identifying types <attribute_types>` associated with each
        attribute.

        These *itypes* dictate how the privacy and quality models
        should treat the underlying data.

        Valid values, specified as case-insensitive strings, are:

        * :ref:`identifying <identifying_attribute>`
        * :ref:`quasi <quasi_identifying_attribute>`
        * :ref:`sensitive <sensitive_attribute>`
        * :ref:`insensitive <insensitive_attribute>`

        These *itypes* can be read via the itypes property:
            >>> prot.itypes
            PassengerId    IDENTIFYING
            Survived       INSENSITIVE
            Pclass         INSENSITIVE
            Name           IDENTIFYING
            Sex                  QUASI
            Age            INSENSITIVE
            SibSp          INSENSITIVE
            Parch          INSENSITIVE
            Ticket         INSENSITIVE
            Fare           INSENSITIVE
            Cabin          INSENSITIVE
            Embarked       INSENSITIVE
            dtype: object

        And be read or set via either the indexing operator:
            >>> prot.itypes['Fare']
            'INSENSITIVE'
            >>> prot.itypes['Fare'] = 'SENSITIVE'

        or via property access:
            >>> prot.itypes.Fare
            'SENSITIVE'
            >>> prot.itypes.Fare = 'INSENSITIVE'

        '''
        return Accessor(self._id_types,
                        transform=lambda val: IdType[val.upper()],
                        callback=partial(_set_id_type_callback,
                                         self._hierarchies))

    @property
    def hierarchies(self):
        '''The *hierarchies* associated with each attribute.'''
        return Accessor(self._hierarchies,
                        validator=partial(_validate_hierarchy, self.df),
                        callback=partial(_set_hierarchy_callback,
                                         self._id_types))

    def _validate_types(self):
        '''Validate that the DataFrame hasn't changed types underneath us'''
        for col in self.df:
            if col not in self._data_types:
                raise ValueError(f'Unknown column {col}')
            ok, msg = _valid_data_type(self.df, col, self._data_types[col])

            if not ok:
                raise ValueError(f'DataFrame modified to contain invalid type '
                                 f'for column {col}: {msg}')

    def _gen_config(self):
        return {
            'delimiter': ',',
            'encoding': 'UTF-8',
            'columns': [self._gen_col_config(col) for col in self.df],
            'globalPrivacyModel': self.privacy_model._get_config(),
            'qualityModelConfig': self.quality_model._get_config(),
            'suppressionLimit': self.suppression,
            'heuristicStepLimit': self.heuristic_step_limit,
            'heuristicSearch': self.heuristic_search,
            'sampleRows': 0
            }

    def _gen_col_config(self, col):
        config = {
            'name': col,
            'dataType': self._data_types[col].name,
            'identifyingType': self._id_types[col].value
            }

        if self._hierarchies.get(col) is not None:
            hierarchy = self._hierarchies[col]
            config[hierarchy._conf_key] = hierarchy._get_config()

        if self._col_privacy_models.get(col) is not None:
            config['privacyModel'] = self._col_privacy_models[col]._get_config()

        return config
