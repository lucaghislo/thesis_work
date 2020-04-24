#!/usr/bin/env python3
# coding=utf8
'''


'''
import pkg_resources

from .__version__ import __version__  # noqa

__all__ = ['__version__', 'Protect']

import jnius_config
jnius_config.add_classpath(
    pkg_resources.resource_filename(__name__, 'jar/protect-0.1.0.jar'))

try:
    import jnius as _  # noqa
except Exception:
    raise RuntimeError('Could not find Java 11; be sure to set JAVA_HOME')

from .protect import Protect  # noqa
