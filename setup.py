r'''
"sogou translate"
'''
# pylint: disable=invalid-name
from pathlib import Path
import re

from setuptools import setup, find_packages

name = """sogou-tr-free"""
description = ' '.join(name.split('-'))
dir_name, = find_packages()

version, = re.findall(r"__version__\W*=\W*'([^']+)'", open(Path(__file__).parent / f'{dir_name}/__init__.py').read())

README_rst = f'{Path(__file__).parent}/README.md'
long_description = open(README_rst, encoding='utf-8').read() if Path(README_rst).exists() else ''

setup(
    name=name,
    packages=find_packages(),
    version=version,
    description=description,
    long_description=long_description,
    keywords="'machine translation' free scraping",
    author="mikeee",
    url=f'http://github.com/ffreemt/{name}',
    classifiers=[
        'Intended Audience :: Users',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT License',
)
