# -*- coding: utf-8 -*-

from paver.easy import path as paver_path
from paver.easy import sh as paver_sh
from paver.easy import *
import paver.misctasks
from paver import setuputils
setuputils.install_distutils_tasks()

import sys, os
import glob
import paver.doctools
from setuptools import find_packages, command

sys.path.insert(0, str(paver_path.getcwd()))

import kitchen.release

options(
    setup = Bunch(
        name=kitchen.release.NAME,
        version=kitchen.release.__version__,
        description=kitchen.release.DESCRIPTION,
        author=kitchen.release.AUTHOR,
        author_email=kitchen.release.EMAIL,
        license=kitchen.release.LICENSE,
        keywords='Useful Small Code Snippets',
        url=kitchen.release.URL,
        download_url=kitchen.release.DOWNLOAD_URL,
        packages=find_packages(),
        include_package_data=True,
        install_requires=[],
        extras_require = {
            'advancedencodingguess' : ['chardet'],
            },
        test_require = ['coverage', 'nose', ],
        build_requires = ['babel', 'paver', 'sphinx'],
        entry_points = {
            },
        message_extractors = {
            'kitchen': [('**.py', 'python', None),]
            },
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python :: 2.3',
            'Programming Language :: Python :: 2.4',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing :: General',
            ],
        ),
    minilib=Bunch(
        extra_files=['doctools']
        ),
    sphinx=Bunch(
        docroot='.',
        builddir='build-doc',
        sourcedir='docs'
        ),
    pylint=Bunch(
        module=['kitchen']
        ),
    publish=Bunch(
        doc_location='fedorahosted.org:/srv/web/releases/k/i/kitchen/docs/',
        tarball_location='fedorahosted.org:/srv/web/releases/k/i/kitchen/'
        ),
    i18n=Bunch(
        builddir='locale',
        installdir='/usr/share/locale',
        domain='kitchen',
        ),
    ### FIXME: These are due to a bug in paver-1.0
    # http://code.google.com/p/paver/issues/detail?id=24
    # Fixed in 1.0.... need EPEL-5 packages for the new paver
    sdist=Bunch(),
    )

@task
@needs(['html'])
def publish_doc():
    options.order('publish', add_rest=True)
    cmd = 'rsync -av build-doc/html/ %s' % (options.doc_location,)
    dry(cmd, paver_sh, cmd)

@task
@needs(['sdist'])
def publish_tarball():
    options.order('publish', add_rest=True)
    tarname = '%s-%s.tar.gz' % (options.name, options.version)
    cmd = 'scp dist/%s %s' % (tarname, options.tarball_location)
    dry(cmd, paver_sh, cmd)

@task
@needs(['publish_doc', 'publish_tarball'])
def publish():
    pass

try:
    import babel.messages.frontend
    has_babel = True
except ImportError:
    has_babel = False

if has_babel:
    @task
    def make_catalogs():
        '''Compile all message catalogs for release'''
        options.order('i18n', add_rest=True)
        for po_file in glob.glob('po/*.po'):
            locale, ext = os.path.splitext(os.path.basename(po_file))
            build_dir = paver_path(os.path.join(options.builddir, locale,
                'LC_MESSAGES'))

            try:
                build_dir.makedirs(mode=0755)
            except OSError, e:
                # paver < 1.0 raises if directory exists
                if e.errno == 17:
                    pass
                else:
                    raise
            if 'compile_catalog' in options.keys():
                defaults = options.compile_catalog
            else:
                defaults = Bunch(domain=options.domain,
                        directory=options.builddir)
                options.compile_catalog = defaults

            defaults.update({'input-file': po_file, 'locale': locale})
            ### FIXME: compile_catalog cannot handle --dry-run on its own
            dry('paver compile_catalog -D %(domain)s -d %(directory)s'
                    ' -i %(input-file)s --locale %(locale)s' % defaults,
                    paver_sh, 'paver compile_catalog -D %(domain)s' \
                        ' -d %(directory)s -i %(input-file)s' \
                        ' --locale %(locale)s' % defaults)
            ### FIXME: Need to get call_task to call this repeatedly
            # because options.compile_catalog has changed
            #dry('paver compile_catalog -D %(domain)s -d %(directory)s'
            #        ' -i %(input-file)s --locale %(locale)s' % defaults,
            #        call_task, 'babel.messages.frontend.compile_catalog', options)

#
# Backends
#

def _apply_root(args, path):
    '''Add the root value to the start of the path'''
    if 'root' in args:
        if path.startswith('/'):
            path = path[1:]
        path = paver_path(os.path.join(args['root'], path))
    else:
        path = paver_path(path)
    return path

def _install_catalogs(args):
    '''Install message catalogs in their proper location on the filesystem.

    Note: To use this with non-default commandline arguments, you must use 
    '''
    # Rebuild message catalogs
    if 'skip_build' not in args and 'skip-build' not in args:
        call_task('make_catalogs')

    options.order('i18n', add_rest=True)
    # Setup the install_dir
    if 'install_catalogs' in args:
        cat_dir = args['install_catalogs']
    elif 'install_data' in args:
        cat_dir = os.path.join(args['install_data'], 'locale')
    else:
        cat_dir = options.installdir

    # Setup the install_dir
    cat_dir = _apply_root(args, cat_dir)

    for catalog in paver_path(options.builddir).walkfiles('*.mo'):
        locale_dir = catalog.dirname()
        path = paver_path('.')
        for index, nextpath in enumerate(locale_dir.splitall()):
            path = path.joinpath(nextpath)
            if paver_path(options.builddir).samefile(path):
                install_locale = cat_dir.joinpath(os.path.join(
                        *locale_dir.splitall()[index + 1:]))
                try:
                    install_locale.makedirs(mode=0755)
                except OSError, e:
                    # paver < 1.0 raises if directory exists
                    if e.errno == 17:
                        pass
                    else:
                        raise
                install_locale = install_locale.joinpath(catalog.basename())
                if install_locale.exists():
                    install_locale.remove()
                dry('cp %s %s'%  (catalog, install_locale),
                        catalog.copy, install_locale)
                dry('chmod 0644 %s'%  install_locale,
                        install_locale.chmod, 0644)

@task
@cmdopts([('root=', None, 'Base root directory to install into'),
    ('install-catalogs=', None, 'directory that locale catalogs go in'),
    ('skip-build', None, 'Skip directly to installing'),
    ])
def install_catalogs():
    _install_catalogs(options.install_catalogs)
    pass

@task
@needs(['make_catalogs', 'setuptools.command.sdist'])
def sdist():
    pass

### FIXME: setuptools.command.install does not respond to --dry-run
@task
@needs(['setuptools.command.install'])
def install():
    '''Override the setuptools install.'''
    _install_catalogs(options.install)

#
# Generic Tasks
#

try:
    from pylint import lint
    has_pylint = True
except ImportError:
    has_pylint = False

if has_pylint:
    @task
    def pylint():
        '''Check the module you're building with pylint.'''
        options.order('pylint', add_rest=True)
        pylintopts = options.module
        dry('pylint %s' % (" ".join(pylintopts)), lint.Run, pylintopts)


@task
def test():
    sh("nosetests --cover-package kitchen --with-cover ")
