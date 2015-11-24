# -*- coding: utf-8 -*-
'''
Generate baseline proxy minion grains
'''
from __future__ import absolute_import
import salt.utils


__proxyenabled__ = ['digital_ocean']

__virtualname__ = 'digital_ocean'


def __virtual__():
    if not salt.utils.is_proxy():
    	# these are grains for a DO proxy minion..
        return False
    else:
        return __virtualname__

