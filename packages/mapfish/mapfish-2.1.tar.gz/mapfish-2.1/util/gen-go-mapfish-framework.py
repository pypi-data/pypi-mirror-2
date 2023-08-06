# 
# Copyright (c) 2008-2011 Camptocamp.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Camptocamp nor the names of its contributors may 
#    be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

#!/usr/bin/env python
"""Generate go-mapfish-framework.py"""
import sys
import textwrap
import virtualenv


after_install = """\
import os, subprocess
def after_install(options, home_dir):
    etc = join(home_dir, 'etc')
    ## TODO: this should all come from distutils
    ## like distutils.sysconfig.get_python_inc()
    if sys.platform == 'win32':
        lib_dir = join(home_dir, 'Lib')
        bin_dir = join(home_dir, 'Scripts')
    elif is_jython:
        lib_dir = join(home_dir, 'Lib')
        bin_dir = join(home_dir, 'bin')
    else:
        lib_dir = join(home_dir, 'lib', py_version)
        bin_dir = join(home_dir, 'bin')

    if not os.path.exists(etc):
        os.makedirs(etc)
    # install mapfish egg
    subprocess.call([join(bin_dir, 'easy_install'),
        '--index-url', 'http://www.mapfish.org/downloads/%s/pkg',
        '--allow-hosts', 'www.mapfish.org',
        'mapfish'])
    # install mapfish.plugin.client egg
    subprocess.call([join(bin_dir, 'easy_install'),
        '--index-url', 'http://www.mapfish.org/downloads/%s/pkg',
        '--allow-hosts', 'www.mapfish.org',
        'mapfish.plugin.client'])

    if sys.platform != 'win32':
        # install mapfish egg
        subprocess.call([join(bin_dir, 'easy_install'),
            '--index-url', 'http://www.mapfish.org/downloads/%s/pkg',
            '--allow-hosts', 'www.mapfish.org',
            'psycopg2'])
    else:
        import urllib2, cStringIO, zipfile
        try:
            # installation of psycopg2 for windows:
            url = 'http://www.mapfish.org/downloads/exe/psycopg2-2.0.10.win32-py2.5-pg8.3.7-release.exe'
            print >> sys.stdout, '\\nDownloading ' + url
            remotezip = urllib2.urlopen(url)
            zipinmemory = cStringIO.StringIO(remotezip.read())
            print >> sys.stdout, 'Processing psycopg2 installation for windows'
            zip = zipfile.ZipFile(zipinmemory)
            for fn in zip.namelist():
                fn_splitted = fn.split('/')[1:] # remove PLATLIB dir
                fn_path = os.path.join(lib_dir, 'site-packages', *fn_splitted)
                if not os.path.exists(os.path.dirname(fn_path)):
                    os.makedirs(os.path.dirname(fn_path))
                f = open(fn_path, 'wb')
                f.write(zip.read(fn))
                f.close()
            print >> sys.stdout, 'Installed ' \\
                     + os.path.abspath(os.path.join(lib_dir,
                                                    'site-packages',
                                                    'psycopg2'))

            # installation of shapely for windows:
            url = 'http://www.mapfish.org/downloads/exe/Shapely-1.0.12.win32.exe'
            print >> sys.stdout, '\\nDownloading ' + url
            remotezip = urllib2.urlopen(url)
            zipinmemory = cStringIO.StringIO(remotezip.read())
            print >> sys.stdout, 'Processing shapely installation for windows'
            zip = zipfile.ZipFile(zipinmemory)

            for fn in zip.namelist():
                fn_splitted = fn.split('/')[1:] # remove DATA and PURELIB dirs
                if fn_splitted[0] == 'DLLs':
                    fn_path = os.path.join(home_dir, *fn_splitted)
                elif fn_splitted[0].endswith('.egg-info'):
                    if fn_splitted[1] == 'PKG-INFO':
                        fn_path = os.path.join(lib_dir, 'site-packages', fn_splitted[0])
                    else:
                        continue
                else:
                    fn_path = os.path.join(lib_dir, 'site-packages', *fn_splitted)
                if not os.path.exists(os.path.dirname(fn_path)):
                    os.makedirs(os.path.dirname(fn_path))
                f = open(fn_path, 'wb')
                f.write(zip.read(fn))
                f.close()
            print >> sys.stdout, 'Installed ' \\
                     + os.path.abspath(os.path.join(lib_dir,
                                                    'site-packages',
                                                    'shapely'))
        except urllib2.HTTPError:
            # handle exception
            print >> sys.stderr, 'Error when downloading. Abort...'
"""

def generate(filename, version):
    # what's commented out below comes from go-pylons.py

    #path = version
    #if '==' in version:
    #    path = version[:version.find('==')]
    #output = virtualenv.create_bootstrap_script(
    #    textwrap.dedent(after_install % (path, version)))

    output = virtualenv.create_bootstrap_script(
        textwrap.dedent(after_install % (version, version, version)))
    fp = open(filename, 'w')
    fp.write(output)
    fp.close()


def main():
    if len(sys.argv) > 2:
        print >> sys.stderr, 'Usage: %s [version]' % sys.argv[0]
        sys.exit(1)
    
    if len(sys.argv) == 2:
        version = sys.argv[1]
        print >> sys.stdout, 'Generating go script for installation of ' \
                'version %s of MapFish' % version
    else:
        version = 'all'
        print >> sys.stdout, 'Version has not been specified:'
        print >> sys.stdout, 'Generating go script for installation of ' \
                'development version of MapFish'

    filename = 'go-mapfish-framework-%s.py' % version
    generate(filename, version)


if __name__ == '__main__':
    main()
