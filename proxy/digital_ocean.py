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

'''
from __future__ import absolute_import

# Import python libs
import logging
import salt.utils.http

HAS_REST_EXAMPLE = True

# This must be present or the Salt loader won't load this module
__proxyenabled__ = ['digital_ocean']


# Variables are scoped to this module so we can have persistent data
# across calls to fns in here.
GRAINS_CACHE = {}
DETAILS = {}

# Want logging!
log = logging.getLogger(__file__)


# This does nothing, it's here just as an example and to provide a log
# entry when the module is loaded.
def __virtual__():
    '''
    Only return if all the modules are available
    '''
    log.debug('digital_ocean proxy __virtual__() called...')
    return True

# Every proxy module needs an 'init', though you can
# just put a 'pass' here if it doesn't need to do anything.


def init(opts):
    log.debug('digital_ocean proxy init() called...')

    # Save the REST URL
    DETAILS['url'] = opts['proxy']['url']

    # Make sure the REST URL ends with a '/'
    if not DETAILS['url'].endswith('/'):
        DETAILS['url'] += '/'


def id(opts):
    '''
    Return a unique ID for this proxy minion.  This ID MUST NOT CHANGE.
    If it changes while the proxy is running the salt-master will get
    really confused and may stop talking to this minion
    '''
    r = salt.utils.http.query(opts['proxy']['url']+'id', decode_type='json', decode=True)
    return r['dict']['id'].encode('ascii', 'ignore')


def grains():
    '''
    Get the grains from the proxied device
    '''
    if not GRAINS_CACHE:
        r = salt.utils.http.query(DETAILS['url']+'info', decode_type='json', decode=True)
        GRAINS_CACHE = r['dict']
    return GRAINS_CACHE


def grains_refresh():
    '''
    Refresh the grains from the proxied device
    '''
    GRAINS_CACHE = {}
    return grains()


