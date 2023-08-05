# -*- coding: utf-8 -*-
import os
from mercurial import util, commands, ui, hg

__all__ = 'QuickStart'.split()

class QuickStart(object):
    data = {
        'templates_dir': '_templates',
        'www_dir': '/tmp/www',
        'media_dir': 'media',
    }

    hgrc = """[talaria]
templates = %(templates_dir)s
media = %(media_dir)s
www = %(www_dir)s"""

    options = """{
    "type": "staticpage",
    "template": "default.html",
    "title": "sample page title",
    "templates": "%(templates_dir)s",
    "media": {"%(media_dir)s":"%(media_dir)s"}
}"""

    template = """<html><head><title>{{ page.title }}</title></head>
   <body>
       {{ page.content }}
   </body>
</html>"""

    content = """
Done. Basic talaria project repository has been created. Now you can change
current working directory to "%(repository_dir)s" and take a glance on the
project structure:

    cd '%(repository_dir)s'
    hg status

Then you can perform some modifications and commit changes:

    hg commit

After these steps you must publish Talaria repository with an appropriate
command:

    hg talaria-publish

Files will be created in the directory %(www_dir)s, so you can view data both
online and offline:

    hg talaria-runserver

Last command runs python demo HTTP server, so you can open an URL
http://localhost:8080 in your browser and check the result. If you're not fully
satisfied with the result, you can change the contents and then update the last
commit by typing:

    hg talaria-publish --amend

Files %(repository_dir)s/.hg/hgrc and %(repository_dir)s/options.json contain
project settings.

Happy hacking!
"""

    def __init__(self, quickstart_data={}):
        self.data.update(quickstart_data)

    def create(self):
        repository_dir = self.data['repository_dir']
        _hg = os.path.join( repository_dir, '.hg')
        if (os.path.isdir(_hg)):
            raise util.Abort('Repository in the directory %s is already'
                 ' created' % self.data['repository_dir'])
        _ui = ui.ui()
        # create repository
        commands.init(_ui, dest=repository_dir)
        # create directories
        for k in 'media_dir templates_dir'.split():
            dirpath = os.path.join(repository_dir, self.data[k])
            os.makedirs(dirpath)
        # create hgrc
        fd = open(os.path.join(repository_dir, '.hg/hgrc'), 'w')
        fd.write(self.hgrc % self.data)
        fd.close()
        # create default options file
        options_file = os.path.join(
            repository_dir, 'options.json'
        )
        fd = open(options_file, 'w')
        fd.write(self.options % self.data)
        fd.close()
        # create template file
        template_file = os.path.join(
            repository_dir, self.data['templates_dir'], 'default.html'
        )
        fd = open(template_file, 'w')
        fd.write(self.template)
        fd.close()
        # create sample content file
        content_file = os.path.join(
            repository_dir, 'content.mkd'
        )
        fd = open(content_file, 'w')
        fd.write(self.content % self.data)
        fd.close()
        # create "keep" media file
        media_file = os.path.join(
            repository_dir, self.data['media_dir'], '.keep'
        )
        fd = open(media_file, 'w')
        fd.close()
        # create hgrepo
        hgrepo = hg.repository(_ui, repository_dir)
        hgrepo.add([
            'content.mkd',
            'options.json',
            os.path.join(self.data['templates_dir'], 'default.html'),
            os.path.join(self.data['media_dir'], '.keep'),
        ])
        return hgrepo
