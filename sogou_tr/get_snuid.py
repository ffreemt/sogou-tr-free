"""
fetch SNIUID
"""

from itertools import dropwhile
import requests

URL = "https://fanyi.sogou.com/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"  # NOQA
HEADERS = {"origin": URL, "User-Agent": UA, "Referer": "https://fanyi.sogou.com/"}


def get_snuid():
    """ get SNUID. """
    return next(
        dropwhile(
            lambda elm: elm[0] != "SNUID",
            requests.get(
                "https://fanyi.sogou.com/", headers=HEADERS
            ).cookies.iteritems(),
        )
    )[1]


SNUID = get_snuid()
