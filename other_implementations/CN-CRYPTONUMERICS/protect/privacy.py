#!/usr/bin/env python3
# coding=utf8

from abc import ABC, abstractmethod
from enum import Enum, auto


__all__ = ['KAnonymity']


class PrivacyModel(ABC):
    def _get_config(self):
        return {
            'privacyModelType': self._model_name,
            'params': self._get_params()
            }

    @abstractmethod
    def _get_params(self):
        pass

    def __repr__(self):
        return f'<{self.__class__.__name__}: {repr(self._get_params())}>'


class GlobalPrivacyModel(PrivacyModel):
    pass


class AttributePrivacyModel(PrivacyModel):
    def _validate(self, col_type, col_kind, col_id, col_hierarchy):
        return True


class KAnonymity(GlobalPrivacyModel):
    '''k-Anonymity privacy model


    Implements a k-Anonymity algorithm as described in *k-anonymity: A
    model for protecting privacy, Sweeney L., 2002*. Requires that at
    least one attribute is set as a quasi-identifier.

    Parameters
    ----------
    k : int
       The **k** parameter as described in the paper, specifying the minimum
       equivalence class size desired.

    '''
    _model_name = 'K_ANONYMITY'

    def __init__(self, k):
        '''

        '''
        self.k = k

    @property
    def k(self):
        '''The **k** parameter itself. Can be read as a property:

            >>> prot.k
            3

        Alternatively, can be used to change the **k** parameter:

            >>> prot.k = 3
        '''
        return self._k

    @k.setter
    def k(self, k):
        try:
            k = int(k)
        except (ValueError, TypeError):
            raise ValueError('Must provide an integer to KAnonymity')
        if k <= 0:
            raise ValueError('KAnonymity requires k >= 1')
        self._k = k

    def _get_params(self):
        return {'k': self.k}


class EDDifferentialPrivacy(GlobalPrivacyModel):
    '''(ε,δ)-Differential Privacy

    Implements (ε,δ)-Differential Privacy using the SafePub algorithm based on
    (k,β)-SDGS.

    Note:  Coming soon. Please contact us for more info at
    `support <mailto:support@cryptonumerics.com>`_\\.

    Parameters
    ----------
    epsilon : float
        The ε parameter for (ε,δ)-Differential Privacy
    delta : float
        The δ parameter for (ε,δ)-Differential Privacy
    degree : str
        Degree of generalization to apply to the dataset. One of 'none', 'low',
        'low_medium', 'medium', 'medium_high', 'high', or 'complete'.
    '''
    _model_name = 'NOT_IMPLEMENTED'

    class DGScheme(Enum):
        NONE = auto()
        LOW = auto()
        LOW_MEDIUM = auto()
        MEDIUM = auto()
        MEDIUM_HIGH = auto()
        HIGH = auto()
        COMPLETE = auto()

    def __init__(self, epsilon, delta, degree=None):
        # XXX: Should we check for very large values?
        raise NotImplementedError('Only available in paid version, please '
                                  'contact support@cryptonumerics.com')
        self.epsilon = epsilon
        self.delta = delta
        self.degree = degree

    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, epsilon):
        try:
            epsilon = float(epsilon)
        except (ValueError, TypeError):
            raise ValueError('Epsilon must be an float')
        if epsilon <= 0:
            raise ValueError('Epsilon must have a positive value')
        self._epsilon = epsilon

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, delta):
        try:
            delta = float(delta)
        except (ValueError, TypeError):
            raise ValueError('Epsilon must be an float')
        if delta <= 0:
            raise ValueError('Delta must have a positive value')
        self._delta = delta

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, degree):
        if degree is None:
            self._degree = None
            return
        try:
            self._degree = EDDifferentialPrivacy.DGScheme[degree.upper()]
        except KeyError:
            raise ValueError(
                f'Invalid generalization degree {degree}, valid values '
                f'are: '
                f'{EDDifferentialPrivacy.DGScheme.__members__.keys()}')

    def _get_params(self):
        params = {
            'epsilon': self.epsilon,
            'delta': self.delta,
            }

        if self.degree is not None:
            params['degree'] = self.degree.name
        return params


# class TCloseness(AttributePrivacyModel):
#     def __init__(self, t, hierarchical=False):
#         self.t = t
#         if hierarchical:
#             self._model_name = 'HIERARCHICAL_DISTANCE_T_CLOSENESS'
#         else:
#             self._model_name = 'EQUAL_DISTANCE_T_CLOSENESS'

#     def _validate(self, col_type, col_kind, col_id, col_hier):
#         if (self._model_name == 'HIERARCHICAL_DISTANCE_T_CLOSENESS'
#             and col_hier is None):
#             raise ValueError('Must supply hierarchies when using t-Closeness '
#                              'in hierarchical mode')
#         return True

#     @property
#     def t(self):
#         return self._t

#     @t.setter
#     def t(self, t):
#         if t <= 0:
#             raise ValueError('t must be greater than 0')
#         try:
#             self._t = t
#         except (ValueError, TypeError):
#             raise ValueError('t must be representable as a float')

#     def _get_params(self):
#         return {'t': self.t}


# class LDiversity(AttributePrivacyModel):
#     def __init__(self, l, entropy=False):
#         self.l = l
#         if entropy:
#             self._model_name = 'ENTROPY_L_DIVERSITY'
#         else:
#             self._model_name = 'DISTINCT_L_DIVERSITY'

#     @property
#     def l(self):
#         return self._l

#     @l.setter
#     def l(self, l):
#         if l <= 0:
#             raise ValueError('l must be greater than 0')
#         try:
#             self._l = l
#         except (ValueError, TypeError):
#             raise ValueError('l must be representable as a float')

#     def _get_params(self):
#         return {'l': self.l}
