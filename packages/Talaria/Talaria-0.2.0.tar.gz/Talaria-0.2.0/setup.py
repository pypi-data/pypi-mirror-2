# -*- coding: utf-8 -*-
from setuptools import setup
setup(
    name = 'Talaria',
    version = '0.2.0',
    packages = ['talaria'],
    install_requires = ['mercurial>=1.3', 'markdown>=2.0', 'Jinja2>=2.2'],
    author = 'Roman Imankulov',
    author_email = 'roman@netangels.ru',
    description = 'Talaria, a geek-friendly content management system',
    license = 'GNU GPLv2+',
    keywords = 'talaria cms mercurial hg static_html',
    url = 'http://www.imankulov.name/talaria/',
    long_description = open('README').read(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Documentation",
    ]
)
