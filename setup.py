r'''
"sogou translate"
'''
# pylint: disable=invalid-name
from pathlib import Path
import re

from setuptools import setup, find_packages  # type: ignore

name = """sogou-tr-free"""
# description = ' '.join(name.split('-'))
description = name.replace('-tr-', ' translate for ')
dir_name, = find_packages()

# version, = re.findall(r"\n__version__\W*=\W*'([^']+)'", open(Path(__file__).parent / f'{dir_name}/__init__.py').read())
version, = re.findall(r"\n__version__\W*=\W*'([^']+)'", open('%s/%s/__init__.py' % (Path(__file__).parent, dir_name)).read())

# README_rst = f'{Path(__file__).parent}/README.md'
README_rst = '%s/README.md' % Path(__file__).parent

long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''

setup(
    name=name,
    packages=find_packages(),
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['machine translation', 'free', 'scraping', ],
    author="mikeee",
    # url=f'http://github.com/ffreemt/{name}',
    url='http://github.com/ffreemt/%s' % name,
    # download_url=f'https://github.com/ffreemt/{name}/archive/v_{version}.tar.gz',
    download_url='https://github.com/ffreemt/{name}/archive/v_%s.tar.gz' % version,
    install_requires=[
        'requests_cache',
        'jmespath',
        'fuzzywuzzy',
        'langid',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
