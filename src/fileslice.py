"""
Functionality pertaining to the globbing/listing of file sources within a filetree.
"""
import os
import glob

class Aiglobber():
    """
    A specific grepper, with a specific configuration, held at a certain spot.

    :param list[str] types: list of valid file extension types, in standard *nix-style wildcarding format.
        Defaults to ["*"] (all files)
    :param str top: top node/directory to begin from. This is for security and performance purposes.
        Defaults to current dir (using python's __file__)
    """
    def __init__(self, types=None, top=os.path.dirname(__file__)):
        self.filetypes = types or ["*"]  # pylint hates this in the constructor for some reason
        self.topdir = top
        self.position = self.topdir

    def aiglob(self, pathchunk):
        """
        Greps files of the configured types from the pathchunk.
        This only returns the *names* of the files, not their paths as python's grep module does.

        :param str pathchunk: path chunk to grep

        :raises AccessDenied: if the requested path is forbidden based on current settings.

        :return: files at the designated position that match the configured types
        :rtype: list[str]
        """
        try:
            newposition = self._updateposition(pathchunk)
        except PathfindingException:
            return []

        if not self._is_subdir(newposition):
            raise AccessDenied(f"{newposition} is not a subdir of {self.topdir}, access is denied.")
        self.position = newposition

        filelist = []
        for pattern in self.filetypes:
            filelist.extend(glob.glob(os.path.join(self.position, pattern)))
        filelist = list(set(filelist))
        return [os.path.basename(filepath) for filepath in filelist]

    def _updateposition(self, pathchunk):
        """
        Finds the updated position based on the path requested to be globbed.
        Handles relative and absolute pathchunks based on current-relative, top-relative, and absolute paths.

        :param str pathchunk: path chunk to attempt to analyze

        :raises PathfindingException: if the given path can truly not be found

        :return: the new position, taking the requested pathchunk into consideration
        :rtype: str
        """
        if os.path.isabs(pathchunk) and os.path.exists(pathchunk):
            return pathchunk
        # Non-absolute paths can be relative paths to the "current" path
        elif os.path.isdir(os.path.join(self.position, pathchunk)):
            return os.path.abspath(os.path.join(self.position, pathchunk))
        # Or relative paths to the top node
        elif os.path.isdir(os.path.join(self.topdir, pathchunk)):
            return os.path.abspath(os.path.join(self.topdir, pathchunk))
        else:
            raise PathfindingException(f"No absolute or relative path found at pathchunk\n{pathchunk}")

    def _is_subdir(self, secondpath):
        """
        Security verification that the requested path is a subdirectory of the top node configured.
        Handles symlinks, using os.path.realpath.
        Python 3.9 introduces pathlib.PurePath.is_relative_to which does this...

        :param str secondpath: path to compare to the top node of this Aiglobber.

        :return: whether secondpath is a subdir of self.topdir
        :rtype: bool
        """
        return os.path.realpath(self.topdir) == os.path.commonpath([os.path.realpath(self.topdir),
                                                                    os.path.realpath(secondpath)])


class PathfindingException(Exception):
    """
    Errors related to unfindable paths.
    """


class AccessDenied(Exception):
    """
    Access to this directory is forbidden based on current settings.
    """
