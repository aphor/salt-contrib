# -*- coding: utf-8 -*-
'''
This is a proxy-minion designed to connect to and communicate with
Digital Ocean APIv2

To assist in migration from salt cloud, the digital_ocean proxy minion is designed
  to be analagous to a salt cloud provider. Like the salt cloud provider it has
  is created with pillars and provides (eventually..) grains to specify
   * API keys
   * bootstrap SSH keys
   * location
  and additional grains to specify
   * account
     - metadata
     - activity log
   * DNS
     - domains
     - records
   * allocated droplets (VMs)
   * available images
   * allocated floating (NAT mapped virtual) IPs

https://docs.saltstack.com/en/latest/topics/proxyminion/index.html
https://docs.saltstack.com/en/develop/topics/topology/proxyminion/index.html
https://docs.saltstack.com/en/develop/topics/proxyminion/demo.html

'''
from __future__ import absolute_import

# Import python libs
import crypt, logging
from salt.utils.decorators import depends
import salt.utils.http

from distutils.version import LooseVersion as _LooseVersion
try:
  import digitalocean as DO # requires https://pypi.python.org/pypi/python-digitalocean
  HAVE_DIGITALOCEAN = lambda _ver_: _LooseVersion(digitalocean.__version__) >= _LooseVersion(_ver_)
except ImportError as DIGITALOCEAN_IMPORT_EXCEPTION:
  log.info('cannot import python-digitalocean')
  HAVE_DIGITALOCEAN = lambda _ver_: False
  log.info(DIGITALOCEAN_IMPORT_EXCEPTION)

# This must be present or the Salt loader won't load this module
__proxyenabled__ = ['digital_ocean']


# Variables are scoped to this module so we can have persistent data
# across calls to fns in here.
GRAINS_CACHE = {}
DETAILS = {}

# Want logging!
log = logging.getLogger(__file__)


def __virtual__():
    '''
    Only load this module if running as a proxy minion and have sufficient version of digitalocean module.
    '''
    if salt.utils.is_proxy() and HAVE_DIGITALOCEAN('1.8'):
        return __virtualname__
    else:
        return False


def init(opts):
    '''
    Populate DETAILS with copy of opts
    '''
    log.debug('digital_ocean proxy init() called...')
    DETAILS.update(opts)


def id(opts):
    '''
    Return a unique ID for this proxy minion.
    This is a crypt() hash of the Digtital Ocean API key.
    If a crypt_salt is specified in options, it will be used to generate the ID.
    '''
    key = opts['proxy']['apikey']
    if 'crypt_salt' in opts['proxy']:
      crypt_salt = opts['proxy']['crypt_salt']
    else:
      crypt_salt = 'DigitalOceanAPIv2'
    return crypt().encode('ascii', 'ignore')


def grains():
    '''
    Get the grains from the proxied device
    '''
    if not GRAINS_CACHE:
        GRAINS_CACHE = {}
        GRAINS_CACHE.update(DETAILS)
        r = salt.utils.http.query(DETAILS['url']+'info', decode_type='json', decode=True)
        GRAINS_CACHE.update(r['dict'])
    return GRAINS_CACHE


def grains_refresh():
    '''
    Refresh the grains from the proxied device
    '''
    GRAINS_CACHE = {}
    return grains()


