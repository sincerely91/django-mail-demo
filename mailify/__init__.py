from receivers import *

__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 0
}

__author__ = 'Keith Hall'
__contact__ = 'code@keith.io'
__homepage__ = "http://www.github.com/keithio/django-mailify/"
__docformat__ = "restructuredtext"
__license__ = "MIT"


def get_version(release_level=True):
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i.%(micro)i" % __version_info__]
    if release_level and __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)


__version__ = get_version()
