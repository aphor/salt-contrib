'''
Execution Module for interacting with DigitalOcean REST APIv2

Requires python-digitalocean module, because some people at DigitalOcean
 contribute to that library, and was recommended by them.

'''

import logging
import salt.utils
from distutils.version import LooseVersion as _LooseVersion
try:
	import digitalocean # requires https://pypi.python.org/pypi/python-digitalocean
	HAS_DIGITALOCEAN = True
except ImportError as DIGITALOCEAN_IMPORT_EXCEPTION:
	log.error('cannot import python-digitalocean')
	HAS_DIGITALOCEAN = False
	log.error(DIGITALOCEAN_IMPORT_EXCEPTION)

def __virtual__():
	'''
	Only load if we have imported a sufficient version of python-digitalocean module and
	  we are running as a proxy minion.
	'''
	if HAS_DIGITALOCEAN and salt.utils.is_proxy() and _LooseVersion(digitalocean.__version__) >= _LooseVersion('1.8'):
		return __virtualname__
	else:
		return False

