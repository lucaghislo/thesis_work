#!/usr/bin/env python3
# coding=utf8

from abc import ABC

__all__ = ['Loss', 'Classification']


class QualityModel(ABC):
    def _get_config(self):
        return {
            'qualityModelType': self._model_name,
            'params': self._get_params()
            }

    def _get_params(self):
        return {}

    def __repr__(self):
        return f'<{self.__class__.__name__}: {repr(self._get_params())}>'


class Loss(QualityModel):
    '''Loss metric

    This model calculates the information loss associated with each
    level of transformation, and attempts to maintain as much
    information as possible in the resulting output.
    '''
    _model_name = 'LOSS_METRIC'


# class Precision(QualityModel):
#     _model_name = 'PRECISION_METRIC'


# class Entropy(QualityModel):
#     _model_name = 'ENTROPY_METRIC'


class Classification(QualityModel):
    '''A quality model that attempts to retain data important for training
    classifiers.

    This model implements the metric as described in
    Iyengar, Vijay S. *Transforming Data to Satisfy Privacy Constraints*.
    Proc Int Conf Knowl Disc Data Mining, p. 279-288 (2002).

    Note: Available only in the commercial version, please contact
    `support <mailto:support@cryptonumerics.com>`_\\.

    Parameters
    ----------
    target_col : str
        The name of the column containing the target/dependent variable

    '''

    _model_name = 'NOT_IMPLEMENTED'

    def __init__(self, target_col):
        '''Test'''
        raise NotImplementedError('Only available in paid version, please '
                                  'contact support@cryptonumerics.com')
        self.target_col = target_col

    @property
    def target_col(self):
        return self._target_col

    @target_col.setter
    def target_col(self, target_col):
        self._target_col = target_col

    def _get_params(self):
        return {'colName': self.target_col}
