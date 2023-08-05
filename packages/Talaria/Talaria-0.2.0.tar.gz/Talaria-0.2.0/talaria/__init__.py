# -*- coding: utf-8 -*-
"""Talaria: a geek friendly CMS system"""
from talaria.loader import *
from talaria.publisher import *
from talaria.pages import *
from talaria.repo import *
from talaria.utils import *
from talaria.quickstart import *

__version__ = '0.2.0'

def ui_publish(ui, hgrepo, **opts):
    """Publish talaria repository

    Publish latest repository changeset (tip) into the directory, defined in
    .hgrc config file.

    An option -r can be used to determine changeset to publish instead of tip.

    An option --amend is used to amend (correct) latest commit instead of
    publishing the selected one. When this option is set, option "-r" has no
    effect.
    """
    from mercurial import util, commands

    publisher = Publisher(hgrepo)
    rev = opts['rev']
    if opts['amend']:
        if rev != 'tip':
            raise util.Abort('Option --amend works only for latest "tip" '
                             'changeset')
        publisher.amend()
    else:
        publisher.publish(hgrepo[rev])


def ui_runserver(ui, hgrepo, **opts):
    """ Run simple web server

    Run web server serving static files in the directory, defined by the "www"
    option in [talaria] section of the config.
    """
    import SimpleHTTPServer
    hostport = opts['bind'].strip().split(':', 1)
    if len(hostport) == 1:
        hostport = ('0.0.0.0', int(hostport[0]))
    else:
        hostport = (hostport[0], int(hostport[1]))
    if opts['root']:
        rootdir = opts['root']
    else:
        repo = Repo(hgrepo, 'tip')
        rootdir = repo.www_dir
    os.chdir(rootdir)
    srv = SimpleHTTPServer.BaseHTTPServer.HTTPServer(
        hostport, SimpleHTTPServer.SimpleHTTPRequestHandler)
    srv.allow_reuse_address = True
    ui.status('Serving %s directory (listen for %s:%d)\n' % (
        rootdir, hostport[0], hostport[1]
    ))
    srv.serve_forever()


def ui_stats(ui, hgrepo, **opts):
    """ Show talaria statistics about repository.

    Show config variables, latest published revision, information whether the
    project is up to date """
    publisher = Publisher(hgrepo)
    rev1 = publisher.published_revision()
    rev2 = publisher.hg['tip']
    uptodate = rev1 == rev2
    repo = Repo(hgrepo, rev1.hex())
    ui.status('Templates directory   :  %s\n' % repo.templates_dir)
    ui.status('Data directory        :  %s\n' % repo.data_dir)
    ui.status('Output www directory  :  %s\n' % repo.www_dir)
    ui.status('Published revision    :  %s\n' % rev1.hex()[:8])
    ui.status('Latest tip revision   :  %s\n' % rev2.hex()[:8])
    ui.status('Project is up to date :  %s\n' % (uptodate and 'YES' or 'NO'))


def ui_quickstart(ui, **opts):
    """ Easy way to create sample talaria project.

    This command can be used to create quickly basic repository layout. This
    layout demonstrates general Talaria project structure and can be used as
    starting point for further modifications.

    Create an empty directory, move there and then type 'hg talaria-quickstart'
    """
    ui.status()
    data = QuickStart.data.copy()
    data['repository_dir'] = os.path.realpath('.')
    ui.status("""
This quickstart master will help you to create basic repository layout. Now you're
going to answer some questions concerning the configuration of the project. Default
values are specified in square brackets.

""")
    options = (
        ('repository_dir',
            'Root repository directory. \n'
            'This directory will contain mercurial repository'
        ),
        ('templates_dir',
            'Directory with Jinja2 templates. \n'
            'The path is relative to the root of repository'
        ),
        ('media_dir',
            'Directory with static media files. \n'
            'This directory may contain js, jpg, css and other static files. \n'
            'The path is relative to the root of repository'
        ),
        ('www_dir',
            'Output www directory. \n'
            'Typically you\'ll want to set up\n'
            'an absolute path like /tmp/www'),

    )
    for option_name, description in options:
        default_value = data.get(option_name, '')
        prompt_string = '%s. [%s]:' % (description, default_value)
        value = ui.prompt(prompt_string, default=default_value).strip()
        if value:
            data[option_name] = value
    qs = QuickStart(data)
    qs.create()
    ui.status(qs.content % qs.data)


cmdtable = {
    'talaria-publish': (
        ui_publish,
        [
            ('r', 'rev', 'tip', 'repository revision to publish'),
            ('', 'amend', False, 'update latest changeset'),
        ],
        "hg talaria-publish [options]",
    ),
    'talaria-runserver': (
        ui_runserver,
        [
            ('b', 'bind', '0.0.0.0:8000', 'colon separated host and port to listen for'),
            ('r', 'root', '', 'root directory of the web server (default is '
                                'the one defined in talaria "www" option'),
        ],
        "hg talaria-runserver [options]",
    ),
    'talaria-stats': (
        ui_stats,
        [ ],
        "hg talaria-stats"
    ),
    'talaria-quickstart': (
        ui_quickstart,
        [ ],
        "hg talaria-quickstart"
    ),
}

from mercurial import commands
commands.norepo += " talaria-quickstart"
