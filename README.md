# sogou-tr-free [![PyPI version](https://badge.fury.io/py/sogou-tr-free.svg)](https://badge.fury.io/py/sogou-tr-free)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sogou translate for free -- local cache, throttling (1.5 calls/s from 1001st call on). Let's hope it lasts.

### Update

version 0.0.10: added `update_snuid`

### Installation
``` pip install -U sogou-tr-free```

or
* Install (pip or whatever) necessary requirements, e.g. ```
pip install requests requests_cache jmespath
fuzzywuzzy``` or ```
pip install -r requirements.txt```
* Drop the file sogou_tr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/sogou-tr-free.git``` or download https://github.com/ffreemt/sogou-tr-free/archive/master.zip and unzip) and change to the sogou-tr-free folder and do a ```
python setup.py develop```

### Usage

```
from sogou_tr import sogou_tr
print(sogou_tr('hello world'))  # -> '你好世界'
print(sogou_tr('hello world', to_lang='de'))  # -> 'Hallo Welt'
print(sogou_tr('hello world', to_lang='fr'))  # -> 'Salut tout le monde'
print(sogou_tr('hello world', to_lang='ja'))  # ->'ハローワールド'
```

#### Speedup
For each request made by `sogou_tr`, a vlaid `SNUID` is reqired. It takes time to acquire a SNUID, however. On the other hand, the SNUID can be used for a certain time period.

Hence, `sogout_tr` has a parameter to control whether to update SNUID or not.  The parameter is, well, called `update_snuid`. By default, `update_snuid=True`. You can turn it off to speed things up:
```
text = "test 1232"
res = sogou_tr(text, update_snuid=False)
```
How do we know the SNUID is still valid? sogou_tr will throw an `Exception("sogou server likely acting up")` when the SNUID is no longer valid. Therefore, we might do something like this:
```
text = "test 1232"
try:
    res = sogou_tr(text, update_snuid=False)
except Exception as exc:
    if "server likely acting up" in str(exc):
        res = sogou_tr(text, update_snuid=True)
```
