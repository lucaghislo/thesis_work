#!/usr/bin/env python3
# coding=utf8

from jnius.reflect import autoclass


ProtectConfig = autoclass(
    'com/cryptonumerics/identification/data/ProtectConfig')
Protect = autoclass('com/cryptonumerics/identification/core/Protect')
ByteArrayInputStream = autoclass('java/io/ByteArrayInputStream')
HashMap = autoclass('java/util/HashMap')
