# baidu-tr-free

Sogou translate for free -- local cache plus throttling. Let's hope it lasts.

### Install
* Install (pip or whatever) necessary requirements, e.g. ```
pip install requests_cache jmespath
fuzzywuzzy``` or ```
pip -r requirements.txt```
* Drop the file sogou_tr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* or clone the repo (e.g., ```git clone git@github.com:ffreemt/sogou-tr-free.git``` or download https://github.com/ffreemt/sogou-tr-free/archive/master.zip and unzip) and change to the sogou-tr-free folder and do a ```
python setup.py develop```

### Usage

```
from sogou_tr import sogou_tr
print(sogou_tr('hello world'))  # -> '你好世界'
print(sogou_tr('hello world', to_lang='de'))  # ->'Hallo Welt'
print(sogou_tr('hello world', to_lang='fr'))  # ->'Salut tout le monde'
print(sogou_tr('hello world', to_lang='ja'))  # ->'ハローワールド'```

### Acknowledgments

* Thanks to everyone whose code was used
