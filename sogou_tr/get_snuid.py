'''
fetch SNIUID
'''

import requests
from itertools import dropwhile

URL = 'https://fanyi.sogou.com/'


def get_snuid():
    ''' get SNUID '''
    return next(dropwhile(lambda elm: elm[0] != 'SNUID', requests.get('https://fanyi.sogou.com/').cookies.iteritems()))[1]

SNUID = get_snuid()
