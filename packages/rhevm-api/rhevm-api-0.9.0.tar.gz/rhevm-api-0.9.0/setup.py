#
# This file is part of RHEVM-API. RHEVM-API is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# RHEVM-API is copyright (c) 2010 by the RHEVM-API authors. See the file
# "AUTHORS" for a complete overview.

import sys
import os.path
import inspect

from distutils.command.build import build
from setuptools import setup, Extension, Command


version_info = {
    'name': 'rhevm-api',
    'version': '0.9.0',
    'description': 'A REST mapping of the PowerShell API of RHEV-M.',
    'author': 'Geert Jansen',
    'author_email': 'geert@boskant.nl',
    'url': 'http://bitbucket.org/geertj/rhevm-api',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application' ]
}


class mybuild(build):

    def _topdir(self):
        fname = inspect.getfile(sys.modules['__main__'])
        absname = os.path.abspath(fname)
        return os.path.split(absname)[0]

    def _store_version(self):
        fname = os.path.join(self._topdir(), 'lib', 'rhevm', '_version.py')
        contents = '# This is a geneated file - do not edit!\n'
        version = tuple(map(int, version_info['version'].split('.')))
        contents += 'version = %s\n' % repr(version)
        try:
            fin = file(fname, 'r')
        except IOError:
            current = None
        else:
            current = fin.read()
            fin.close()
        if contents != current:
            fout = file(fname, 'w')
            fout.write(contents)
            fout.close()

    def run(self):
        self._store_version()
        build.run(self)


setup(
    package_dir = { '': 'lib' },
    packages = ['rhevm', 'rhevm.module', 'rhevm.test'],
    test_suite = 'nose.collector',
    entry_points = { 'console_scripts': [
            'rhevm-api-cmdline = rhevm.server:main',
            'rhevm-api-isapi = rhevm.iis:main'] },
    install_requires = ['winpexpect >= 1.4', 'python-rest >= 1.3',
                        'pyyaml >= 3.09'],
    cmdclass = { 'build': mybuild },
    **version_info
)
