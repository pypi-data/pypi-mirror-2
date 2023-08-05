# -*- coding: utf-8 -*-
r"""
>>> from mercurial import ui, hg
>>> from jinja2 import Environment

>>> repo = hg.repository(ui.ui(), '../talaria-test')

>>> loader = HgLoader(repo[0], 'templates')
>>> env = Environment(loader=loader)
>>> env.get_template('default.html')
<Template 'default.html'>
>>> env.get_template('page2_custom.html')
Traceback (most recent call last):
    ...
TemplateNotFound: page2_custom.html

>>> loader = HgLoader(repo[1], 'templates')
>>> env = Environment(loader=loader)
>>> env.get_template('page2_custom.html')
<Template 'page2_custom.html'>

"""
import os
import jinja2
from talaria.utils import HgPath

__all__ = 'HgLoader'.split()

class HgLoader(jinja2.BaseLoader):

    def __init__(self, changectx, template_directory=''):
        self.changectx, self.template_directory = changectx, template_directory
        self.path = HgPath(self.changectx)

    def get_source(self, environment, template):
        filename = os.path.join(self.template_directory, template)
        if not self.path.isfile(filename):
            err = jinja2.TemplateNotFound(template)
            err.args = ('Template not found',)
            raise err
        source = self.path.data(filename).decode('utf-8')
        return (source, None, lambda: True,)
