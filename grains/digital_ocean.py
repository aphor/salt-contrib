# -*- coding: utf-8 -*-
'''
Generate baseline proxy minion grains
'''
from __future__ import absolute_import
import salt.utils


__proxyenabled__ = ['digital_ocean']

__virtualname__ = 'digital_ocean'

from distutils.version import LooseVersion as _LooseVersion
try:
  import digitalocean as DO # requires https://pypi.python.org/pypi/python-digitalocean
  HAVE_DIGITALOCEAN = lambda _ver_: _LooseVersion(digitalocean.__version__) >= _LooseVersion(_ver_)
except ImportError as DIGITALOCEAN_IMPORT_EXCEPTION:
  log.info('cannot import python-digitalocean')
  HAVE_DIGITALOCEAN = lambda _ver_: False
  log.info(DIGITALOCEAN_IMPORT_EXCEPTION)


def __virtual__():
    if not (salt.utils.is_proxy() and ):
    	# these are grains for a DO proxy minion..
        return False
    else:
        return __virtualname__

def kernel():
    return {'kernel': 'proxy'}


def os():
    return {'os': 'DigitalOceanRESTAPIv2'}


def location():
    return {'location': 'In this darn virtual machine.  Let me out!'}


def os_family():
    return {'os_family': 'RESTAPI'}


def os_data():
    return {'os_data': 'DigitalOceanRESTAPIv2'}