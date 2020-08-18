# pylint: disable=line-too-long
r"""
TODO：fetch window.seccode from httml
    https://fanyi.sogou.com/logtrace

sogou_tr.py
含10小时本地缓存，非缓存访问限流从1001次开始平均每次 0.67秒

UUID changed 2019-09-06
    pypi-projects\sogou-tr-free\other-projects\tk-secode.js
    function tk(a,c){var d,e,f,g,h,i;for(d=c.split("."),e=Number(d[0])||0,f=[],g=0,h=0;h<a.length;h++)i=a.charCodeAt(h),128>i?f[g++]=i:(2048>i?f[g++]=192|i>>6:(55296==(64512&i)&&h+1<a.length&&56320==(64512&a.charCodeAt(h+1))?(i=65536+((1023&i)<<10)+(1023&a.charCodeAt(++h)),f[g++]=240|i>>18,f[g++]=128|63&i>>12):f[g++]=224|i>>12,f[g++]=128|63&i>>6),f[g++]=128|63&i);for(a=e,g=0;g<f.length;g++)a+=f[g],a=b(a,"+-a^+6");return a=b(a,"+-3^+b+-f"),a^=Number(d[1])||0,0>a&&(a=(2147483647&a)+2147483648),a%=1e6,a.toString()+(a^e)}
    window.seccode=tk(12,"2344578");

var V = window.seccode,
    J = s("" + R + O + M + V),
    W = {
        "from": R,
        "to": O,
        "text": M,
        "client": "pc",
        "fr": "browser_pc",
        "pid": "sogou-dict-vr",
        "dict": !0,
        "word_group": !0,
        "second_query": !0,
        "uuid": B,
        "needQc": f.need,
        "s": J
    };

obsolet：
UUID can be obtained in the following way:
js_url = 'https://dlweb.sogoucdn.com/translate/pc/static/js/app.55db663a.js'
js_str = requests.get(js_url).text
_ = re.findall(r'var\sV=s\(""\+P\+O\+M\+"(\w+)?"\)', js_str)
UUID = _[0] if _ else ''
assert len(UUID) == 32

cache and throttle (avg 0.5 sec) for non-cache requests

playground\sogou-fanyi\sogou_tr.py
"""
# import logging
from pathlib import Path
from time import sleep
from random import random, randint  # pylint: disable=unused-import
import hashlib

# from uuid import uuid4

from langid import classify

# import pytest

import requests
import requests_cache  # type: ignore

# import browser_cookie3

from jmespath import search  # type: ignore
from fuzzywuzzy import fuzz, process  # type: ignore

from logzero import logger

from sogou_tr.get_snuid import get_snuid
from sogou_tr.get_snuid import SNUID

# from gevent import monkey  # fix: RecursionError: maximum recursion depth exceeded while calling a Python object
# monkey.patch_all(ssl=False)

# LOGGER = logging.getLogger(__name__)
# LOGGER.addHandler(logging.NullHandler())

# for ipython copy-n-paste test
if "__file__" not in globals():
    __file__ = "ipython_sessioin.py"

HOME_FOLDER = Path.home()
CACHE_NAME = (HOME_FOLDER / Path(__file__).stem).as_posix()
EXPIRE_AFTER = 36000

_ = """
requests_cache.install_cache()
requests_cache.core.configure(
    cache_name=CACHE_NAME,
    expire_after=EXPIRE_AFTER,
    allowable_codes=(200, ),
    allowable_methods=('GET', 'POST')
)  # post ok
# """

URL0 = "https://fanyi.sogou.com"
URL = "https://fanyi.sogou.com/reventondc/translateV2"


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"  # NOQA
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"  # NOQA
HEADERS = {
    "origin": URL0,
    "User-Agent": UA,
    "Referer": "https://fanyi.sogou.com/",
    # 'Pragma': 'no-cache',
    "Cookie": "SNUID=%s" % SNUID,
}

UUID = "4f80db82-1c5f-49ce-840e-838d26598f69"  # 20190929
UUID = "8954e2993f18dd83fd05e79bd6dd040e"  # valid？
UUID = "0e1baf18-e5cb-4387-b6d5-01914cd94f68"
SECCODE = "8511813095151"  # V
# https://fanyi.sogou.com devtools/source logtrace
SECCODE = "8511813095152"  # V 20190929

COOKIES = {
    "IPLOC": "CN8100",
    "SNUID": "FC9528E6393CAD49060771DA3ABE23B8",
    "SUID": "C5AC12DFAF67900A000000005DCFBF87",
    "ABTEST": "7|1573896071|v17",
}

# SESS = requests.Session()
SESS = requests_cache.CachedSession(
    cache_name=CACHE_NAME, expire_after=EXPIRE_AFTER, allowable_methods=("GET", "POST"),
)

# SESS.cookies.update(COOKIES)

SOGOUTR_CODES = [
    "auto",
    "ar",
    "et",
    "bg",
    "pl",
    "ko",
    "bs-Latn",
    "fa",
    "mww",
    "da",
    "de",
    "ru",
    "fr",
    "fi",
    "tlh-Qaak",
    "tlh",
    "hr",
    "otq",
    "ca",
    "cs",
    "ro",
    "lv",
    "ht",
    "lt",
    "nl",
    "ms",
    "mt",
    "pt",
    "ja",
    "sl",
    "th",
    "tr",
    "sr-Latn",
    "sr-Cyrl",
    "sk",
    "sw",
    "af",
    "no",
    "en",
    "es",
    "uk",
    "ur",
    "el",
    "hu",
    "cy",
    "yua",
    "he",
    "zh-CHS",
    "it",
    "hi",
    "id",
    "zh-CHT",
    "vi",
    "sv",
    "yue",
    "fj",
    "fil",
    "sm",
    "to",
    "ty",
    "mg",
    "bn",
]  # pylint: disable=C0301  # NOQA

# https://github.com/imWildCat/sogou-translate/blob/master/sogou_translate.py
ERROR_DICT = {
    "1001": "Translate API: Unsupported language type",
    "1002": "Translate API: Text too long",
    "1003": "Translate API: Invalid PID",
    "1004": "Translate API: Trial PID limit reached",
    "1005": "Translate API: PID traffic too high",
    "1006": "Translate API: Insufficient balance",
    "1007": "Translate API: Random number does not exist",
    "1008": "Translate API: Signature does not exist",
    "1009": "Translate API: The signature is incorrect",
    "10010": "Translate API: Text does not exist",
    "1050": "Translate API: Internal server error",
}


def make_throttle_hook(timeout=1):
    r"""
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached

    time.sleep(min(0, timeout - 0.5) + random())
        average delay: timeout

    s = requests_cache.CachedSession()
    s.hooks = {'response': make_throttle_hook(0.1)}
    s.get('http://httpbin.org/delay/get')
    s.get('http://httpbin.org/delay/get')
    """

    def hook(response, *args, **kwargs):  # pylint: disable=unused-argument
        if not getattr(response, "from_cache", False):
            # print(f'sleeping {timeout} s')

            timeout0 = min(0, timeout - 0.5 + random())
            logger.debug("sleeping %s", timeout0)

            sleep(timeout0)
        return response

    return hook


SESS.hooks = {"response": make_throttle_hook()}
# SESS.get(URL0)
SESS.get("https://fanyi.sogou.com/#auto/zh-CHS/test%201111")


# fmt: off
def sogou_tr(  # pylint: disable=too-many-locals,  too-many-statements, too-many-branches, too-many-arguments,  # noqa: C901
        text,
        from_lang="auto",
        to_lang="zh",
        cache=True,
        fuzzy=True,
        timeout=(55, 66),
        update_snuid: bool = True,  # if Exception("server acting up" turn this on
):
    # fmt: on
    """
    text='my people my country'; from_lang='auto'; to_lang='zh'; cache=True

    pytest --doctest-modules sogou_tr.py

    >>> trtext = sogou_tr('test ' + str(randint(1, 1000)))
    >>> trtext[:2] in '测试试验'
    True
    >>> trtext = sogou_tr('teste', from_lang='de')
    >>> trtext[:2] in '测试试验'
    True
    >>> trtext = sogou_tr('teste', from_lang='de', to_lang='en')
    >>> trtext.lower() in 'test'
    True
    >>> trtext = sogou_tr('teste', from_lang='de', to_lang='een')
    >>> 'invalid' in trtext
    False
    """
    if update_snuid:
        SNUID = get_snuid()  # pylint: disable=redefined-outer-name, invalid-name
        HEADERS.update({"Cookie": "SNUID=%s" % SNUID})

    try:
        text = text.strip()
    except Exception as exc:  # pragma: no cover
        logger.error(exc)
        sogou_tr.text = str(exc)
        text = ""
    if not text:
        sogou_tr.text = "nothing to do"
        return ""

    from_lang = from_lang.lower()
    to_lang = to_lang.lower()

    if from_lang == "auto" and to_lang == "auto":
        to_lang = "zh"

    if from_lang in ["zh", "chinese"]:
        from_lang = "zh-CHS"
    if to_lang in ["zh", "chinese"]:
        to_lang = "zh-CHS"

    if fuzzy:
        if from_lang not in SOGOUTR_CODES:
            from_lang = process.extractOne(
                from_lang, SOGOUTR_CODES, scorer=fuzz.UWRatio
            )[
                0
            ]  # NOQA
        if to_lang not in SOGOUTR_CODES:
            to_lang = process.extractOne(to_lang, SOGOUTR_CODES, scorer=fuzz.UWRatio)[
                0
            ]  # NOQA

    if from_lang == to_lang:
        sogou_tr.text = "nothing to do"
        return text

    # str_ = 'auto' + 'zh-CHS' + text + UUID
    # SECDOE = TK(12,"2344578")  # key = TK(12,"2344578")  # '8511813095151'

    str_ = from_lang + to_lang + text + SECCODE
    md5 = hashlib.md5(str_.encode("utf-8"))
    sign = md5.hexdigest()

    # uuid = uuid4()  # pylint: disable=unused-variable
    data = {
        "client": "pc",
        "dict": "true",
        "fr": "browser_pc",
        "from": from_lang,
        "needQc": "1",
        "pid": "sogou-dict-vr",
        "s": sign,
        "second_query": "true",
        "text": text,
        "to": to_lang,
        # 'uuid': str(uuid),
        "word_group": "true",
    }

    _ = """
    try:
        resp = SESS.post(URL, data=data, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        sogou_tr.text = resp.text
    except Exception as exc:
        logger.error('SESS.post error: %s', exc)
        sogou_tr.text = {"error": str(exc)}
    """
    # del _

    def fetch():
        """fetch"""
        try:
            resp = SESS.post(
                URL,
                data=data,
                # data=data0,
                headers=HEADERS,
                # headers=headers,
                timeout=timeout,
                # cookies=COOKIES,
            )
            resp.raise_for_status()
            sogou_tr.text = resp.text
        except Exception as exc:  # pragma: no cover
            logger.error(exc)
            # resp.json = {'error': str(exc)}
            # resp = str(exc)
            # raise
            sogou_tr.text = {"error": str(exc)}
            resp = requests.models.Request()
            resp.status_code = 499
            resp._contend = str(  # pylint: disable=protected-access
                {"error": str(exc)}
            ).encode()
        return resp

    if cache:
        resp = fetch()
    else:
        with requests_cache.disabled():
            resp = fetch()

    try:
        jdata = resp.json()
    except Exception as exc:  # pragma: no cover
        logger.error("resp.json error: %s", exc)
        jdata = {"json error": str(exc), "errorCode": "21"}

    sogou_tr.json = jdata

    # sometimes capture verification is required
    # unsuccessful verification results in jdata.get('translate').get('errorCode') 20
    try:
        tr_error = jdata.get("translate").get("errorCode")
    except Exception as exc:
        tr_error = str(exc)
    # normal: jdata.get('data') is not None
    if tr_error and jdata.get("data") is None:
        logger.info("jdata: %s", jdata)
        logger.error(
            "get('translate').get('errorCode') error: %s, maybe because daily free quota exceeded or capture verification required \n (acccess http://fanyi.sogou.com to verify)",
            tr_error,
        )

        return None

    try:
        trtext = search("data.translate.dit", jdata)
    except Exception as exc:
        logger.error("jmespath search('data.translate.dit' error: %s", exc)
        trtext = str(exc)

    if not trtext:  # pragma: no cover

        trtext = jdata.get("info")
        if trtext is None:
            trtext = ""

        if "unknown error" in trtext:
            # trtext += f' -- maybe invalid target language [{to_lang}]'
            trtext += " -- maybe invalid target language [%s]" % to_lang

    # failed that
    if not trtext:  # pragma: no cover
        trtext = sogou_tr.text

    # raise Exception(" sogou server acting up")
    langid_ = classify(trtext)
    if langid_[0] not in [to_lang[:2]]:
        logger.warning(
            " to_lang: %s, detected lang: %s, trans text: %s",
            to_lang,
            langid_[0],
            trtext[:40],
        )
        raise Exception(" sogou server likely acting up")
    if langid_[1] > 0:
        logger.warning(" lang detection confidence level to low: %s", langid_[1])
        raise Exception(" sogou server likely acting up")

    # SNUID = getsnuid() update HEADERS.update('Cookie': 'SNUID=%s' % SNUID,}) and retry?

    return trtext


# py.test --log-cli-level=10 sogou_tr.py --cov-report html --cov-report term --cov=sogou_tr  # NOQA
def test_default():
    """test default"""
    text = "this is a test."
    trtext = sogou_tr(text)
    assert "这" in trtext


def test_empty_text():
    """test empty input"""
    text = " "
    trtext = sogou_tr(text)
    assert trtext == ""


def test_fromlang_zh():
    """from_lang=zh"""
    text = "测试"
    trtext = sogou_tr(text, from_lang="zh", to_lang="en")
    assert "test" in trtext


def test_auto_auto():
    """auto auto"""
    text = "test"
    trtext = sogou_tr(text, to_lang="auto")
    assert trtext in "测试实验试验"


def test_from_to_same():
    """from_lang to_lang the same"""
    text = "test"
    trtext = sogou_tr(text, from_lang="zh")
    assert trtext == text


def test_from_fuzzy():
    """from_lang fuzzy match"""
    text = "test"
    trtext = sogou_tr(text, from_lang="een")
    assert trtext in "测试实验试验"


def test_to_fuzzy():
    """to_lang fuzzy match"""
    text = "test"
    trtext = sogou_tr(text, to_lang="zhs")
    assert trtext in "测试实验试验"


def test_cache_false():
    """cache set to False"""
    text = "test"
    trtext = sogou_tr(text, cache=0)
    assert trtext in "测试实验试验"


def test_fuzzy_false():
    """fuzzy set to False"""
    text = "test"
    trtext = sogou_tr(text, fuzzy=0, to_lang="dde")
    assert "invalid" in trtext


def main():  # pragma: no cover
    """main"""
    import sys

    # log_fmt = '%(filename)10s %(lineno)4d %(levelname)6s: %(message)s'
    # logging.basicConfig(format=log_fmt, level=20)

    if len(sys.argv) < 2:
        text = "test this " + str(randint(1, 100000))
        print(f"Provide some text, using [{text}] to test")
        # sys.exit(0)
    else:
        text = " ".join(sys.argv[1:])
    print(sogou_tr(text), "\n")

    print(sogou_tr(text, to_lang="de"))
    print(sogou_tr(text, to_lang="fr"))
    print(sogou_tr(text, to_lang="es"))

    print(sogou_tr(text, to_lang="dde"))


if __name__ == "__main__":
    main()  # pragma: no cover
