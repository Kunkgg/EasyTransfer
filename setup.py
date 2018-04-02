# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys
import os
# sys.path.insert(0,os.path.abspath('easytransfer'))
setup(
    name='easytransfer',
    version='0.1',
    packages=find_packages(),
    include_packge_data=True,
    install_requires=[
        'click', 'Flask', 'requests'
],
    package_data={'easytransfer': ['templates/*.html']},
    entry_points="""
        [console_scripts]
        easytr=easytransfer.easytransfer:cli
""",)
