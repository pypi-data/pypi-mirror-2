# Copyright (C) 2010  Martin von Gagern
#
# This file is part of bzr-bash-completion
#
# bzr-bash-completion free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the
# License, or (at your option) any later version.
#
# bzr-bash-completion is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# http://doc.bazaar.canonical.com/developers/plugin-api.html#metadata-protocol
# describes these variables, which have to be imported into setup.py.
bzr_plugin_name = 'bash_completion'
bzr_commands = [ 'bash-completion' ]

# Have a look at bzrlib._format_version_tuple for info about version 5-tuples,
# and at http://packages.python.org/distribute/setuptools.html#specifying-your-project-s-version
# for information about how python versions do compare with setuptools
bzr_plugin_version = (1, 0, 1, 'final', 0)

# http://doc.bazaar.canonical.com/developers/plugin-api.html#plugin-version
# describes another version tuple:
version_info = bzr_plugin_version

# And we also want a string representation, matching the output generated by
# bzrlib._format_version_tuple, but avoiding its sanity checks.
__version__ = '.'.join([str(x) for x in version_info[:3]])
if version_info[3] == 'final':
    __version__ = "%d.%d.%d" % version_info[:3]
elif version_info[4] == 0:
    __version__ = "%d.%d.%d%s" % version_info[:4]
else:
    __version__ = "%d.%d.%d%s%d" % version_info
