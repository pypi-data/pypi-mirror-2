#
import os
import warnings
from paste.script import pluginlib

from quintagroup.themetemplate.qplone3_theme import qPlone3Theme

warned = False

def getEggInfo(output_dir):
    """ Return path to egg info directory, raise error if not found.
    """
    egg_info = pluginlib.find_egg_info_dir(output_dir)
    assert egg_info is not None, "egg_info directory must present for the package"

    return egg_info


def getThemeVarsFP(egg_info):
    """ Return file system path to theme vars configurations
    """
    global warned
    old_path = os.path.join(egg_info, 'theme_vars.txt')
    if os.path.exists(old_path):
        if not warned:
            warnings.warn(
                "In 1.0 version theme variables from <the.theme.package>/theme_vars.cfg " \
                "file only will be used. Currently " \
                "<the.theme.package>/<the.theme.package>.egg_info/theme_vars.txt " \
                "also supported." , DeprecationWarning, 2)
            warned = True
        return old_path
    return os.path.join(egg_info, '..', 'theme_vars.cfg')
