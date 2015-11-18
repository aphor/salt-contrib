# -*- coding: utf-8 -*-
'''
    :codeauthor: David Boucha
    :copyright: © 2014 by the SaltStack Team, see AUTHORS for more details.
    :license: Apache 2.0, see LICENSE for more details.


    salt.grains.digitalocean_metadata.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Create a DigitalOcean grain from the DigitalOcean metadata server.
    See https://developers.digitalocean.com/metadata/#metadata-in-json

    Note that not all datacenters were supported when this feature was first
    released.
'''

# Import Python Libs
import requests


def digitalocean():
    '''
    Return DigitalOcean metadata.
    '''
    salt.utils.warn_until(
        'Carbon',
        'grains.digitalocean_metadata is deprecated (Digital Ocean APIv1 is no longer avaialble). ' +
        'This module will be removed in SaltStack Carbon. Please use grains.digitalocean (APIv2) instead.')

    do_svr = 'http://169.254.169.254/metadata/v1.json'
    metadata = requests.get(do_svr)

    if metadata.status_code == 200:
        return {'digitalocean': metadata.json()}
    return {'digitalocean': []}
