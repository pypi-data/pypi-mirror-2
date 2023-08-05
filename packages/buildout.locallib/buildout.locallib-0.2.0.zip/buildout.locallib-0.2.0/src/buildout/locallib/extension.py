from zc.buildout import easy_install
from distutils.sysconfig import get_python_lib
import pkg_resources
import os
import logging
logger = logging.getLogger('buildout.locallib')

SP_PATH = get_python_lib()

class Installer(easy_install.Installer):
    """ hook easy_install.Installer() for egg search path modification """

    base = None

    def __init__(self, *args, **kw):
        # if exist args[5] (is path parameter) or 'path' keyword argument,
        # update path list for including 'site-packages' path.

        logger.debug('easy_install.Installer hooked.')
        if len(args) > 5:
            path = args[5]
        elif kw.get('path') is not None:
            path = kw['path']
        else:
            path = kw['path'] = []

        if SP_PATH not in path:
            path.append(SP_PATH)

        self.base.__init__(self, *args, **kw)

    __init__.func_doc = easy_install.Installer.__init__.func_doc


def patch_to_Installer(buildout):
    if easy_install.Installer != Installer:
        logger.debug('easy_install.Installer patched')
        Installer.base = easy_install.Installer
        easy_install.Installer = Installer

def create_dummy_egglink(base, name, location):
    link_name = '%s.egg-link' % name
    link_path = os.path.join(base, link_name)
    if not os.path.exists(link_path):
        logger.info('create dummy egg-link: %s', link_path)
        f = open(link_path, 'wt')
        f.write(location)
        f.write("\n../\n")
        f.close()
    else:
        # file was exist. need update?
        pass

def create_dummy_egginfo(base, name, version):
    egg_name = '%(name)s-%(version)s.egg-info' % locals()
    egg_path = os.path.join(base, egg_name)
    if not os.path.exists(egg_path):
        logger.info('create dummy egg-info: %s', egg_path)
        open(egg_path, 'wt').close() # create empty file.


def construct_dummy_infos(buildout):
    # TODO: print warning if newest=true.
    # this extension use site-package's package, but if newest mode is
    # enabled then setuptools get newest version than specified version
    # at 'locallibs' parameter.
    # if you using locallibs parameter, run buildout with -N options.

    bo = buildout['buildout']

    if 'locallibs' in bo:
        locallibs = buildout.get(bo['locallibs'], {})
    else:
        return # buildout secsion has no 'locallibs' key.

    for key,name in locallibs.items():
        req = pkg_resources.Requirement.parse(name)
        try:
            info = pkg_resources.get_provider(req)
            # expected package are exist (include no-version-specified).
            # Installer patch make to find this.
            create_dummy_egglink(
                    bo['develop-eggs-directory'],
                    info.key, info.location)
            create_dummy_egginfo(
                    bo['develop-eggs-directory'],
                    info.key, info.version)
        except pkg_resources.VersionConflict,e:
            # find another version (except no-version-specified).
            create_dummy_egginfo(
                    bo['develop-eggs-directory'],
                    req.key, req.specs[0][1])
        except pkg_resources.DistributionNotFound,e:
            # maybe using 'simple installed package' (no egg-info extention)
            if not req.specs:
                raise pkg_resources.ExtractionError("%r expect 'name==version' value format." % req.key)
            create_dummy_egginfo(
                    bo['develop-eggs-directory'],
                    req.key, req.specs[0][1])


def load(buildout):
    patch_to_Installer(buildout)
    construct_dummy_infos(buildout)

