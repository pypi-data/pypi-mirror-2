#
# This file is part Contentbus

# Contentbus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Contentbus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Contentbus.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
from os import path
from glob import glob
import contentbus

setup(
    name = 'contentbus',
    version = contentbus.__version__,
    license = 'GPL',
    description='Content-based bus',
    long_description = 'Contentbus is an implementation of a content-based publish/subscribe bus, with advanced filter features on messages',
    author = 'Alberto Donato',
    author_email = '<alberto.donato@gmail.com>',
    maintainer = 'Alberto Donato',
    maintainer_email = '<alberto.donato@gmail.com>',
    url = 'http://code.google.com/p/contentbus',
    download_url = 'http://code.google.com/p/contentbus/downloads/list', 
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data = True,
    scripts = glob(path.join('bin', '*')),
    keywords = 'content content-based bus publish subscribe',
    classifiers = [ 'Development Status :: 2 - Pre-Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: GNU General Public License (GPL)',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Software Development :: Libraries :: Application Frameworks',
                    'Topic :: Software Development :: Libraries :: Python Modules',
                    ]
    )
