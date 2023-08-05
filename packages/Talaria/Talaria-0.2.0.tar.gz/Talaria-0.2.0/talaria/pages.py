# -*- coding: utf-8 -*-
import glob, os, markdown, jinja2

from talaria.loader import HgLoader
from talaria.utils import HgPath, DescriptiveString

__all__ = 'BasePage StaticPage PhotoAlbumPage Image'.split()


class BasePage(object):
    """ Main page class

    In fact this one is nothing but extended storage for attributes, which
    used to build the page upon a given template

    Base part of the page attributes is given from the options.json hierarchy,
    the rest of them is defined by the class itself
    """

    type = 'unknown'

    def __init__(self, repo, path, **kwargs):
        if '..' in path:
            raise ValueError, 'Path cannot contain ".." symbols'
        path = path.strip('/')
        self.repo, self.path = repo, path
        for k, v in self.repo.get_options(self.path).items():
            setattr(self, k, v)

    def www_path(self):
        return os.path.join(self.repo.www_dir, self.path)

    def template_path(self):
        return os.path.join(self.repo.templates_dir, self.path)

    def data_path(self):
        return os.path.join(self.repo.data_dir, self.path)

    def get_children(self, recursive=False):
        return self.repo.get_children(self, recursive)

    def get_parent(self):
        return self.repo.get_parent(self)

    def __eq__(self, otherpage):
        if not isinstance(otherpage, BasePage):
            return False
        return self.repo == otherpage.repo \
                and self.path == otherpage.path

    def __ne__(self, otherpage):
        return not self.__eq__(otherpage)

    def __str__(self):
        return 'Page %s (%s)' % (self.type, self.path)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.path)


class StaticPage(BasePage):

    type = 'staticpage'

    def __init__(self, repo, path, **kwargs):
        super(StaticPage, self).__init__(repo, path, **kwargs)
        # get data from files
        for basename, filename in self.get_data_files():
            content = self.repo.hgpath.data(filename)
            content = content.decode('utf8', 'ignore')
            if filename.endswith('mkd'):
                md = markdown.Markdown(
                    extensions=self.repo.markdown_extensions)
                attr = DescriptiveString(md.convert(content))
                attr.source_type = 'markdown'
                attr.source = content
                attr.filename = os.path.basename(filename)
            else:
                attr = DescriptiveString(content)
                attr.source = content
                attr.source_type = 'html'
                attr.filename = os.path.basename(filename)
            setattr(self, basename, attr)


    def get_data_files(self):
        """ Return list of markdown or plain HTML files

        Get the list of files, each of which ends with .html or .mkd
        and resides in the page's directory and returns a list of tuples:

        - basename of the file (i.e. "hello" for "hello.mkd" or "hello.html")
        - pathname to the file relative to repository root
        """
        mkd_filenames = self.repo.hgpath.glob(self.data_path(), '*.mkd')
        html_filenames = self.repo.hgpath.glob(self.data_path(), '*.html')
        for filename in mkd_filenames + html_filenames:
            basename = '.'.join(filename.split('.')[:-1])
            absname = os.path.join(self.data_path(), filename)
            if self.repo.hgpath.isfile(absname):
                yield (basename, absname)

    def get_template(self):
        """ Return ready to parse template """
        return self.repo.template_env.get_template(self.template)

    def get_dependencies(self):
        """ Return a set of dependent pages """
        return [f[1] for f in self.get_data_files()]

    def render(self):
        """ Return parsed page """
        return self.get_template().render(dict(page=self))

    def save(self):
        """ Save page in the filesystem """
        dirname = self.www_path()
        filename = os.path.join(dirname, 'index.html')
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        fd = open(filename, 'w')
        fd.write(self.render().encode('utf-8', 'ignore'))
        fd.close()

    def delete(self):
        """ Remove page from www directory """
        dirname = self.www_path()
        filename = os.path.join(dirname, 'index.html')
        if os.path.isfile(filename):
            os.unlink(filename)
        if os.path.isdir(dirname) and not os.listdir(dirname):
            os.rmdir(dirname)

from PIL import Image as image
from cStringIO import StringIO


class Image(object):


    def _thumbnail_path(self, path):
        chunks = path.rsplit('.', 1)
        attrs = {}
        if len(chunks) == 2:
            attrs['basename'], attrs['ext'] = chunks
        else: # len(chunks) == 1
            attrs['basename'] = chunks[0]
            attrs['ext'] = ''
        return self.thumbnail_template % attrs

    def __init__(self, page, path, description):
        self.page, self.path, self.description = page, path, description
        self.thumbnail_template = getattr(self.page, 'thumbnail_template',
                u'%(basename)s_t.%(ext)s')
        self.thumbnail = self._thumbnail_path(path)
        self.data_path = os.path.join(self.page.data_path(), path)
        self.image_object = image.open(
            StringIO(self.page.repo.hgpath.data(self.data_path))
        )
        self.thumbnail_size = getattr(self.page, 'thumbnail_size', (100, 100))
        self.thumbnail_method = getattr(self.page, 'thumbnail_method', 'resize')
        self.width, self.height = self.image_object.size

    def save(self):
        if not os.path.isdir(self.page.www_path()):
            os.makedirs(self.page.www_path())
        filename = os.path.join(self.page.www_path(), self.path)
        fd = open(filename, 'w')
        self.image_object.save(fd)
        fd.close()

    def save_thumbnail(self):
        if not os.path.isdir(self.page.www_path()):
            os.makedirs(self.page.www_path())
        filename = os.path.join(self.page.www_path(), self.thumbnail)
        fd = open(filename, 'w')
        thumbnail = getattr(self, 'do_' + self.thumbnail_method)()
        thumbnail.save(fd)
        fd.close()

    def delete(self):
        filename = os.path.join(self.page.www_path(), self.path)
        if os.path.isfile(filename):
            os.unlink(filename)

    def delete_thumbnail(self):
        filename = os.path.join(self.page.www_path(), self.thumbnail)
        if os.path.isfile(filename):
            os.unlink(filename)

    # creating thumbnails methods
    def do_thumbnail(self):
        """ create a thumbnail which fits in the given with and height """
        thumbnail = self.image_object.copy()
        thumbnail.thumbnail(self.thumbnail_size, image.ANTIALIAS)
        self.thumbnail_width, self.thumbnail_height = thumbnail.size
        return thumbnail

    def do_resize(self):
        """ create a thumbnail with width and height exactly as defined in the
        thumbnail_size (all pages with the same size). Although, the image can
        be shrinked vertically or horizontally """
        thumbnail = self.image_object.resize(self.thumbnail_size, image.ANTIALIAS)
        self.thumbnail_width, self.thumbnail_height = thumbnail.size
        return thumbnail




class PhotoAlbumPage(StaticPage):
    """ Extended static page which can make photoalbum.

    options.json parameters:

    - thumbnail_size: array of two integers (width and height) for thumbnails to
      create
    - thumbnail_method: either "thumbnail" or "resize" string. The "thumbnail"
      option save  the width/height ratio of the original image, while "resize"
      create the thumbnail exactly with the size of "thumbnail_size".

    filesystem parameters:

    *.jpg: al JPEG files within page directory are handled as image objects,
    each of which have to be added to the .images property of the page.
    Moreover, for every of that images the thumbnail will be created.

    description.txt: file with short description of every image in format
        filename.jpg short description
        filename2.jpg another description
        ...
        etc

    additional properties and methods:

    get_images(): return an array of Image objects, each of which has the set
    of useful fields:

    - path: filename of the image (relative to the page path)
    - description: description of the page as defined in the
      description.txt
    - thumbnail: the name of the thumbnail (currently "filename_t.jpg")
    - width and height: size dimensions of the original image
    - thumbnail_width and thumbnail_height: real size dimensions of the
      thumbnail (may differ from page.thumbnail_size)
    """

    type = 'photoalbum'


    def __init__(self, *args, **kwargs):
        super(PhotoAlbumPage, self).__init__(*args, **kwargs)
        self._image_description = {}
        # get image description lines
        description_filename = os.path.join(
            self.data_path(), 'description.txt')
        if self.repo.hgpath.isfile(description_filename):
            description_text = self.repo.hgpath.data(description_filename)
            for line in description_text.splitlines():
                try:
                    filename, description = line.split(None, 1)
                except ValueError: # need more than 1 value to unpack
                    pass
                self._image_description[filename.strip()] = description.strip()


    def get_images(self):
        filenames = self.repo.hgpath.glob(self.data_path(), '*.jpg')
        for filename in filenames:
            yield Image(self, filename, self._image_description.get(filename))


    def save(self):
        super(PhotoAlbumPage, self).save()
        for image in self.get_images():
            image.save()
            image.save_thumbnail()

    def delete(self):
        for image in self.get_images():
            image.delete()
            image.delete_thumbnail()
        super(PhotoAlbumPage, self).delete()

    def get_dependencies(self):
        deps = super(PhotoAlbumPage, self).get_dependencies()
        filenames = self.repo.hgpath.glob(self.data_path(), '*.jpg')
        for filename in filenames:
            deps.append(os.path.join(self.data_path(), filename))
        return deps
