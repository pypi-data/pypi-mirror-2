# -*- coding: utf-8 -*-
import os
import jinja2

try:
    import json
except ImportError:
    import simplejson as json
from mercurial import ui, hg, util

from talaria.utils import HgPath
from talaria.graph import Digraph
from talaria.loader import HgLoader

__all__ = 'Repo'.split()


class Repo(object):
    """
    Repository gets options from the root options.json.

    name: templates
    default: "_templates"
    description:
    Path to templates directory

    name: media
    default: {}
    description:
    Information about files and directories considered as media (static) files.
    Should be a dictionary where key is a name of file/directory within
    project, whereas value is a path to this object inside the directory to
    export

    name: markdown_extensions
    default: []

    name: page_modules
    default: []
    """

    def __init__(self, hgrepo, revision):
        self.hg, self.revision = hgrepo, revision
        self.changectx = hgrepo[revision]
        self.hgpath = HgPath(self.changectx)
        self.data_dir = ''
        options = self.get_options()

        # hg options
        self.www_dir = self.hg.ui.config(
                'talaria', 'www', 'www').rstrip('/')
        # local options
        self.templates_dir = options.get(
                'templates', '_templates').rstrip('/')
        self.media = options.get('media', {})
        self.markdown_extensions = options.get('markdown_extensions', [])
        self.page_modules = options.get('page_modules', [])
        self.page_modules.insert(0, 'talaria.pages')
        self.path = os.path.dirname(self.hg.path)
        self.loader = HgLoader(self.changectx, self.templates_dir)
        self.template_env = jinja2.Environment(loader=self.loader)
        self.__page_cache = {}
        self.__page_types = None

    def page_types(self):
        """ Build dict: Page type -> page class.

        Returned dict comprises "default classes" along with the classes gathered
        from additional modules defined in "page_modules" variable.
        """
        if self.__page_types is None:
            from talaria.pages import BasePage
            self.__page_types = {}
            for module in self.page_modules:
                mod = __import__(module, globals={}, locals={}, fromlist=['*'])
                for classname, classobj in mod.__dict__.iteritems():
                    try:
                        if issubclass(classobj, BasePage) and classobj != BasePage:
                            self.__page_types[classobj.type] = classobj
                    except TypeError:
                        pass
        return self.__page_types

    def get_options(self, path=''):
        """
        Get the full parameters and options list for the page given by its
        path. Read consecutively all `options.json` files starting with data
        dir until the last one.

        For the URL:
            http://.../page/subpage/subsubpage/
        path:
            page/subpage/subsubpage
        these files will be readed:
            data/options.json
            data/page/options.json
            data/page/subpage/options.json
            data/page/subpage/subsubpage/options.json

        There is also a set of "unheritable options" which can be possesed only
        by a page but not by its children. Currently this set contains only one
        option with name "id".

        TODO: make cache
        path: string with no initial or trailing slash
        """
        path_items = path.strip('/').split('/')
        path_items.insert(0, '')
        curdir = self.data_dir
        options = {}
        for item in path_items:
            curdir = os.path.join(curdir, item)
            opts_file = os.path.join(curdir, 'options.json')
            if self.hgpath.isfile(opts_file):
                data = json.loads(self.hgpath.data(opts_file))
                options.update(data)
        return options

    def build_dependency_tree(self):
        from jinja2 import meta
        self.dependency_tree = Digraph()
        # add template files
        template_files = []
        for f in self.hgpath.files:
            if f.startswith(self.templates_dir):
                template_files.append(f)
                self.dependency_tree.add_node(f, type='file')
        # calculate template dependencies
        for f in template_files:
            template_data = self.hgpath.data(f).decode('utf-8')
            template_deps = list(meta.find_referenced_templates(
                self.template_env.parse(template_data)
            ))
            template_deps = [\
                os.path.join(self.templates_dir, d) for d \
                in template_deps if d is not None  \
            ]
            for dep in template_deps:
                self.dependency_tree.add_edge(dep, f)
        # add options.json files
        options_files = []
        for f in self.hgpath.files:
            if os.path.basename(f) == 'options.json':
                options_files.append(f)
                self.dependency_tree.add_node(f, type='file')
        for child in options_files:
            dchild = os.path.dirname(child)
            for parent in options_files:
                if parent == child:
                    continue
                dparent = os.path.dirname(parent)
                if dchild.startswith(dparent):
                    self.dependency_tree.add_edge(parent, child)
        # add pages
        for page in self.get_pages():
            self.dependency_tree.add_node(page, type='page')
            options_file = os.path.join(page.data_path(), 'options.json')
            if options_file in options_files:
                self.dependency_tree.add_edge(options_file, page)
            try:
                template_file = os.path.join(self.templates_dir, page.template)
            except AttributeError, e:
                raise util.Abort(u'Template for page %r is not defined' % page)
            if template_file in template_files:
                self.dependency_tree.add_edge(template_file, page)
            # add page dependencies
            for filename in page.get_dependencies():
                if filename not in self.dependency_tree.nodes():
                    self.dependency_tree.add_node(filename)
                self.dependency_tree.add_edge(filename, page)

    def has_page(self, path):
        """ Has page returns True only if some files or directories do exist in
        that directory """
        fullpath = os.path.join(self.data_dir, path.strip('/'))
        return self.hgpath.isdir(fullpath)

    def get_page(self, path):
        """ Get page with given path
        path: string with no initial or trailing slash
        """
        # __page_cache utilization is a crucial point, we don't have to create
        # different exemplars of the same page. Instead, dependency tree will
        # break
        if not self.has_page(path):
            raise ValueError, 'page %s does not exist' % path
        if path not in self.__page_cache.keys():
            options = self.get_options(path)
            page_type = options.get('type', 'staticpage')
            try:
                PageClass = self.page_types()[page_type]
            except KeyError:
                raise ValueError('Can\'t define page type "%s"' % page_type)
            page = PageClass(self, path)
            self.__page_cache[path] = page
        return self.__page_cache[path]

    def get_root(self):
        return self.get_page('/')

    def is_empty(self):
        return not self.hgpath.files

    def get_pages(self):
        """Iterator which yields recursively all site pages (Page objects). """
        if self.is_empty():
            return
        root = self.get_root()
        yield root
        for page in root.get_children(recursive=True):
            yield page

    def get_children(self, page, recursive=False):
        """ Iterator which yields (recursively or not) all children of this
        page (Page objects) """
        root = os.path.join(self.data_dir, page.path)
        excluded_items = self.media.keys() + [self.templates_dir,]
        if self.hgpath.isdir(root):
            for fname in self.hgpath.listdir(root):
                relpath = os.path.join(page.path, fname)
                abspath = os.path.join(root, fname)
                if abspath not in excluded_items and self.hgpath.isdir(abspath):
                    pg = self.get_page(relpath)
                    yield pg
                    if recursive:
                        for child in self.get_children(pg, recursive):
                            yield child

    def get_parent(self, page):
        dirname = page.path
        return self.get_page(str(os.path.dirname(dirname)))
