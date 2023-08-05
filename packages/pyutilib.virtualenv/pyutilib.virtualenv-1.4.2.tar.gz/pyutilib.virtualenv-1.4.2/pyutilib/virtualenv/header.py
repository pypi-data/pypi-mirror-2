#  _________________________________________________________________________
#
#  PyUtilib: A Python utility library.
#  Copyright (c) 2008 Sandia Corporation.
#  This software is distributed under the BSD License.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  _________________________________________________________________________
#
#
# This script was created with the virtualenv_install script.
#

import commands
import re
import urllib2
import zipfile
import shutil
import string
import textwrap
import sys
import glob
import errno
import stat

using_subversion = True

#
# The following taken from PyUtilib
#
if (sys.platform[0:3] == "win"): #pragma:nocover
   executable_extension=".exe"
else:                            #pragma:nocover
   executable_extension=""


def search_file(filename, search_path=None, implicitExt=executable_extension, executable=False,         isfile=True):
    if search_path is None:
        #
        # Use the PATH environment if it is defined and not empty
        #
        if "PATH" in os.environ and os.environ["PATH"] != "":
            search_path = string.split(os.environ["PATH"], os.pathsep)
        else:
            search_path = os.defpath.split(os.pathsep)
    for path in search_path:
      if os.path.exists(os.path.join(path, filename)) and \
         (not isfile or os.path.isfile(os.path.join(path, filename))):
         if not executable or os.access(os.path.join(path,filename),os.X_OK):
            return os.path.abspath(os.path.join(path, filename))
      if os.path.exists(os.path.join(path, filename+implicitExt)) and \
         (not isfile or os.path.isfile(os.path.join(path, filename+implicitExt))):
         if not executable or os.access(os.path.join(path,filename+implicitExt),os.X_OK):
            return os.path.abspath(os.path.join(path, filename+implicitExt))
    return None

#
# PyUtilib Ends
#


#
# The following taken from pkg_resources
#
component_re = re.compile(r'(\d+ | [a-z]+ | \.| -)', re.VERBOSE)
replace = {'pre':'c', 'preview':'c','-':'final-','rc':'c','dev':'@'}.get

def _parse_version_parts(s):
    for part in component_re.split(s):
        part = replace(part,part)
        if not part or part=='.':
            continue
        if part[:1] in '0123456789':
            yield part.zfill(8)    # pad for numeric comparison
        else:
            yield '*'+part

    yield '*final'  # ensure that alpha/beta/candidate are before final

def parse_version(s):
    parts = []
    for part in _parse_version_parts(s.lower()):
        if part.startswith('*'):
            if part<'*final':   # remove '-' before a prerelease tag
                while parts and parts[-1]=='*final-': parts.pop()
            # remove trailing zeros from each series of numeric parts
            while parts and parts[-1]=='00000000':
                parts.pop()
        parts.append(part)
    return tuple(parts)
#
# pkg_resources Ends
#

#
# Use pkg_resources to guess version.
# This allows for parsing version with the syntax:
#   9.3.2
#   8.28.rc1
#
def guess_release(svndir):
    if using_subversion:
        output = commands.getoutput('svn ls '+svndir)
        if output=="":
            return None
        #print output
        versions = []
        for link in re.split('/',output.strip()):
            tmp = link.strip()
            if tmp != '':
                versions.append( tmp )
        #print versions
    else:
        if sys.version_info[:2] <= (2,5):
            output = urllib2.urlopen(svndir).read()
        else:
            output = urllib2.urlopen(svndir, timeout=30).read()
        if output=="":
            return None
        links = re.findall('\<li>\<a href[^>]+>[^\<]+\</a>',output)
        versions = []
        for link in links:
            versions.append( re.split('>', link[:-5])[-1] )
    latest = None
    latest_str = None
    for version in versions:
        if version is '.':
            continue
        v = parse_version(version)
        if latest is None or latest < v:
            latest = v
            latest_str = version
    if latest_str is None:
        return None
    return svndir+"/"+latest_str



def zip_file(filename,fdlist):
    zf = zipfile.ZipFile(filename, 'w')
    for file in fdlist:
        if os.path.isdir(file):
            for root, dirs, files in os.walk(file):
                for fname in files:
                    if fname.endswith('exe'):
                        zf.external_attr = (0777 << 16L) | (010 << 28L)
                    else:
                        zf.external_attr = (0660 << 16L) | (010 << 28L)
                    zf.write(join(root,fname))
        else:
            zf.write(file)
    zf.close()


def unzip_file(filename, dir=None):
    fname = os.path.abspath(filename)
    zf = zipfile.ZipFile(fname, 'r')
    if dir is None:
        dir = os.getcwd()
    for file in zf.infolist():
        name = file.filename
        if name.endswith('/') or name.endswith('\\'):
            outfile = os.path.join(dir, name)
            if not os.path.exists(outfile):
                os.makedirs(outfile)
        else:
            outfile = os.path.join(dir, name)
            parent = os.path.dirname(outfile)
            if not os.path.exists(parent):
                os.makedirs(parent)
            OUTPUT = open(outfile, 'wb')
            OUTPUT.write(zf.read(name))
            OUTPUT.close()
    zf.close()



class Repository(object):

    svn_get='checkout'
    easy_install_path = ["easy_install"]
    python = "python"
    svn = "svn"
    dev = []

    def __init__(self, name, root=None, trunk=None, stable=None, release=None, tag=None, pyname=None, pypi=None, dev=False, username=None, install=True, rev=None):
        class _TEMP_(object): pass
        self.config = _TEMP_()
        self.config.name=name
        self.config.root=root
        self.config.trunk=trunk
        self.config.stable=stable
        self.config.release=release
        self.config.tag=tag
        self.config.pyname=pyname
        self.config.pypi=pypi
        if dev == 'True' or dev is True:
            self.config.dev=True
        else:
            self.config.dev=False
        self.config.username=username
        if install == 'False' or install is False:
            self.config.install=False
        else:
            self.config.install=True
        self.config.rev=rev
        self.initialize(self.config)

    def initialize(self, config):
        self.name = config.name
        self.root = config.root
        self.trunk = None
        self.trunk_root = None
        self.stable = None
        self.stable_root = None
        self.release = None
        self.tag = None
        self.release_root = None
        #
        self.pypi = config.pypi
        if not config.pypi is None:
            self.pyname=config.pypi
        else:
            self.pyname=config.pyname
        self.dev = config.dev
        if config.dev:
            Repository.dev.append(config.name)
        self.pkgdir = None
        self.pkgroot = None
        if config.username is None or '$' in config.username:
            self.svn_username = []
        else:
            self.svn_username = ['--username', config.username]
        if config.rev is None:
            self.rev=''
            self.revarg=[]
        else:
            self.rev='@'+config.rev
            self.revarg=['-r',config.rev]
        self.install = config.install

    def guess_versions(self, offline=False):
        if not self.config.root is None:
            if using_subversion:
                rootdir_output = commands.getoutput('svn ls ' + self.config.root)
            else:
                if sys.version_info[:2] <= (2,5):
                    rootdir_output = urllib2.urlopen(self.config.root).read()
                else:
                    rootdir_output = urllib2.urlopen(self.config.root, timeout=30).read()
            try:
                self.trunk = self.config.root+'/trunk'
                self.trunk_root = self.trunk
            except urllib2.HTTPError:
                self.trunk = None
                self.trunk_root = None
            try:
                if offline or not 'stable' in rootdir_output:
                    raise IOError
                self.stable = guess_release(self.config.root+'/stable')
                self.stable_root = self.stable
            except (urllib2.HTTPError,IOError):
                self.stable = None
                self.stable_root = None
            try:
                if offline or not 'releases' in rootdir_output:
                    raise IOError
                self.release = guess_release(self.config.root+'/releases')
                self.tag = None
                self.release_root = self.release
            except (urllib2.HTTPError,IOError):
                try:
                    if offline or not 'tags' in rootdir_output:
                        raise IOError
                    self.release = guess_release(self.config.root+'/tags')
                    self.tag = self.release
                    self.release_root = self.release
                except (urllib2.HTTPError,IOError):
                    self.release = None
                    self.release_root = None
        if not self.config.trunk is None:
            if self.trunk is None:
                self.trunk = self.config.trunk
            else:
                self.trunk += self.config.trunk
        if not self.config.stable is None:
            if self.stable is None:
                self.stable = self.config.stable
            else:
                self.stable += self.config.stable
        if not self.config.release is None:
            if self.release is None:
                self.release = self.config.release
            else:
                self.release += self.config.release
        if not self.config.tag is None:
            if self.release is None:
                self.release = self.config.tag
            else:
                self.release += self.config.tag


    def write_config(self, OUTPUT):
        config = self.config
        print >>OUTPUT, '[%s]' % config.name
        if not config.root is None:
            print >>OUTPUT, 'root=%s' % config.root
        if not config.trunk is None:
            print >>OUTPUT, 'trunk=%s' % config.trunk
        if not config.stable is None:
            print >>OUTPUT, 'stable=%s' % config.stable
        if not config.tag is None:
            print >>OUTPUT, 'tag=%s' % config.tag
        elif not config.release is None:
            print >>OUTPUT, 'release=%s' % config.release
        if not config.pypi is None:
            print >>OUTPUT, 'pypi=%s' % config.pypi
        elif not config.pyname is None:
            print >>OUTPUT, 'pypi=%s' % config.pyname
        print >>OUTPUT, 'dev=%s' % str(config.dev)
        print >>OUTPUT, 'install=%s' % str(config.install)
        if not config.rev is None:
            print >>OUTPUT, 'rev=%s' % str(config.rev)
        if not config.username is None:
            print >>OUTPUT, 'username=%s' % str(config.username)


    def find_pkgroot(self, trunk=False, stable=False, release=False):
        if trunk:
            if self.trunk is None:
                if not self.stable is None:
                    self.find_pkgroot(stable=True)
                elif self.pypi is None:
                    self.find_pkgroot(release=True)
                else:
                    # use easy_install
                    self.pkgdir = None
                    self.pkgroot = None
                    return
            else:
                self.pkgdir = self.trunk
                self.pkgroot = self.trunk_root
                return

        elif stable:
            if self.stable is None: 
                if not self.release is None:
                    self.find_pkgroot(release=True)
                elif self.pypi is None:
                    self.find_pkgroot(trunk=True)
                else:
                    # use easy_install
                    self.pkgdir = None
                    self.pkgroot = None
                    return
            else:
                self.pkgdir = self.stable
                self.pkgroot = self.stable_root
                return

        elif release:
            if self.release is None:
                if not self.stable is None:
                    self.find_pkgroot(stable=True)
                elif self.pypi is None:
                    self.find_pkgroot(trunk=True)
                else:
                    # use easy_install
                    self.pkgdir = None
                    self.pkgroot = None
                    return
            else:
                self.pkgdir = self.release
                self.pkgroot = self.release_root

        else:
            raise IOError, "Must have one of trunk, stable or release specified"
            

    def install_trunk(self, dir=None, install=True, preinstall=False, offline=False):
        self.find_pkgroot(trunk=True)
        self.perform_install(dir=dir, install=install, preinstall=preinstall, offline=offline)
        
    def install_stable(self, dir=None, install=True, preinstall=False, offline=False):
        self.find_pkgroot(stable=True)
        self.perform_install(dir=dir, install=install, preinstall=preinstall, offline=offline)
        
    def install_release(self, dir=None, install=True, preinstall=False, offline=False):
        self.find_pkgroot(release=True)
        self.perform_install(dir=dir, install=install, preinstall=preinstall, offline=offline)
        
    def perform_install(self, dir=None, install=True, preinstall=False, offline=False):
        if self.pkgdir is None:
            self.easy_install(install, preinstall, dir, offline)
            return
        print "-----------------------------------------------------------------"
        print "  Installing branch"
        print "  Checking out source for package",self.name
        print "     Subversion dir: "+self.pkgdir
        if os.path.exists(dir):
            print "     No checkout required"
            print "-----------------------------------------------------------------"
        else:
            print "-----------------------------------------------------------------"
            self.run([self.svn]+self.svn_username+[Repository.svn_get,'-q',self.pkgdir+self.rev, dir])
        if install:
            if self.dev:
                self.run([self.python, 'setup.py', 'develop'], dir=dir)
            else:
                self.run([self.python, 'setup.py', 'install'], dir=dir)

    def update_trunk(self, dir=None):
        self.find_pkgroot(trunk=True)
        self.perform_update(dir=dir)

    def update_stable(self, dir=None):
        self.find_pkgroot(stable=True)
        self.perform_update(dir=dir)

    def update_release(self, dir=None):
        self.find_pkgroot(release=True)
        self.perform_update(dir=dir)

    def perform_update(self, dir=None):
        if self.pkgdir is None:
            self.easy_upgrade()
            return
        print "-----------------------------------------------------------------"
        print "  Updating branch"
        print "  Updating source for package",self.name
        print "     Subversion dir: "+self.pkgdir
        print "     Source dir:     "+dir
        print "-----------------------------------------------------------------"
        self.run([self.svn,'update','-q']+self.revarg+[dir])
        if self.dev:
            self.run([self.python, 'setup.py', 'develop'], dir=dir)
        else:
            self.run([self.python, 'setup.py', 'install'], dir=dir)

    def Xsdist_trunk(self, format='zip'):
        if self.trunk is None:
            if not self.pypi is None:
                self.easy_install()
            elif not self.stable is None:
                self.sdist_stable(format=format)
            else:
                self.sdist_release(format=format)
        else:
            self.pkgdir=self.trunk
            self.pkgroot=self.trunk_root
            print "-----------------------------------------------------------------"
            print "  Checking out source for package",self.name
            print "     Subversion dir: "+self.trunk
            print "-----------------------------------------------------------------"
            self.run([self.svn]+self.svn_username+[Repository.svn_get,'-q',self.trunk, 'pkg'+self.name+self.rev])
            self.run([self.python, 'setup.py', 'sdist','-q','--dist-dir=..', '--formats='+format], dir='pkg'+self.name)
            os.chdir('..')
            rmtree('pkg'+self.name)

    def Xsdist_stable(self, format='zip'):
        if self.stable is None:
            if not self.pypi is None:
                self.easy_install()
            elif not self.release is None:
                self.install_release()
            elif not self.trunk is None:
                self.install_trunk()
        else:
            self.pkgdir=self.stable
            self.pkgroot=self.stable_root
            print "-----------------------------------------------------------------"
            print "  Checking out source for package",self.name
            print "     Subversion dir: "+self.stable
            print "     Source dir:     "+dir
            print "-----------------------------------------------------------------"
            self.run([self.svn]+self.svn_username+[Repository.svn_get,'-q',self.stable, dir])
            self.run([self.python, 'setup.py', 'develop'], dir=dir)

    def Xsdist_release(self, dir=None):
        if self.release is None:
            if not self.pypi is None:
                self.easy_install()
            elif not self.stable is None:
                self.install_stable()
            elif not self.trunk is None:
                self.install_trunk()
        else:
            self.pkgdir=self.release
            self.pkgroot=self.release_root
            print "-----------------------------------------------------------------"
            print "  Checking out source for package",self.name
            print "     Subversion dir: "+self.release
            print "     Source dir:     "+dir
            print "-----------------------------------------------------------------"
            self.run([self.svn]+self.svn_username+[Repository.svn_get]+self.rev+['-q',self.release, dir])
            self.run([self.python, 'setup.py', 'install'], dir=dir)

    def easy_install(self, install, preinstall, dir, offline):
        try:
            if install:
                #self.run([self.easy_install_path, '-q', self.pypi])
                if offline:
                    self.run([self.python, 'setup.py', 'install'], dir=dir)
                else:
                    self.run(self.easy_install_path + ['-q', self.pypi])
            elif preinstall: 
                if not os.path.exists(dir):
                    self.run(self.easy_install_path + ['-q', '--editable', '--build-directory', '.', self.pypi], dir=os.path.dirname(dir))
        except OSError, err:
            print "-----------------------------------------------------------------"
            print "Warning!!! Ignoring easy_install error '%s'" % str(err)
            print "-----------------------------------------------------------------"

    def easy_upgrade(self):
        self.run(self.easy_install_path + ['-q', '--upgrade', self.pypi])

    def run(self, cmd, dir=None):
        cwd=os.getcwd()
        if not dir is None:
            os.chdir(dir)
            cwd=dir
        print "Running command '%s' in directory %s" % (" ".join(cmd), cwd)
        call_subprocess(cmd, filter_stdout=filter_python_develop, show_stdout=True)
        if not dir is None:
            os.chdir(cwd)


if sys.platform.startswith('win'):
    if not is_jython:
        Repository.python += '.exe'
    Repository.svn += '.exe'


def filter_python_develop(line):
    if not line.strip():
        return Logger.DEBUG
    for prefix in ['Searching for', 'Reading ', 'Best match: ', 'Processing ',
                   'Moving ', 'Adding ', 'running ', 'writing ', 'Creating ',
                   'creating ', 'Copying ']:
        if line.startswith(prefix):
            return Logger.DEBUG
    return Logger.NOTIFY


def apply_template(str, d):
    t = string.Template(str)
    return t.safe_substitute(d)


wrapper = textwrap.TextWrapper(subsequent_indent="    ")


class Installer(object):

    def __init__(self):
        self.description="This script manages the installation of packages into a virtual Python installation."
        self.home_dir = None
        self.default_dirname='python'
        self.abshome_dir = None
        self.sw_packages = []
        self.sw_dict = {}
        self.cmd_files = []
        self.auxdir = []
        self.config=None
        self.config_file=None
        self.README="""
#
# Virtual Python installation generated by the %s script.
#
# This directory is managed with virtualenv, which creates a
# virtual Python installation.  If the 'bin' directory is put in
# user's PATH environment, then the bin/python command can be used
# without further installation.
#
# Directories:
#   admin      Administrative data for maintaining this distribution
#   bin        Scripts and executables
#   dist       Python packages that are not intended for development
#   include    Python header files
#   lib        Python libraries and installed packages
#   src        Python packages whose source files can be
#              modified and used directly within this virtual Python
#              installation.
#   Scripts    Python bin directory (used on MS Windows)
#
""" % sys.argv[0]

    def add_repository(self, *args, **kwds):
        if not 'root' in kwds and not 'pypi' in kwds and not 'release' in kwds and not 'trunk' in kwds and not 'stable' in kwds:
            raise IOError, "No repository info specified for repository "+args[0]
        repos = Repository( *args, **kwds)
        self.sw_dict[repos.name] = repos
        self.sw_packages.append( repos )

    def add_dos_cmd(self, file):
        self.cmd_files.append( file )

    def add_auxdir(self, package, todir, fromdir):
        self.auxdir.append( (todir, package, fromdir) )

    def modify_parser(self, parser):
        self.default_windir = 'C:\\'+self.default_dirname
        self.default_unixdir = './'+self.default_dirname
        #
        parser.add_option('--debug',
            help='Configure script to generate debugging IO and to raise exceptions.',
            action='store_true',
            dest='debug',
            default=False)

        parser.add_option('--trunk',
            help='Install trunk branches of Python software.',
            action='store_true',
            dest='trunk',
            default=False)

        parser.add_option('--stable',
            help='Install stable branches of Python software.',
            action='store_true',
            dest='stable',
            default=False)

        parser.add_option('--update',
            help='Update all Python packages.',
            action='store_true',
            dest='update',
            default=False)

        parser.add_option('--proxy',
            help='Set the HTTP_PROXY environment with this option.',
            action='store',
            dest='proxy',
            default=None)

        parser.add_option('--preinstall',
            help='Prepare an installation that will be used to build a MS Windows installer.',
            action='store_true',
            dest='preinstall',
            default=False)

        parser.add_option('--offline',
            help='Perform installation offline, using source extracted from ZIP files.',
            action='store_true',
            dest='offline',
            default=False)

        parser.add_option('--zip',
            help='Add ZIP files that are use define this installation.',
            action='append',
            dest='zip',
            default=[])

        parser.add_option('--use-pythonpath',
            help="By default, the PYTHONPATH is ignored when installing.  This option allows the 'easy_install' tool to search this path for related Python packages, which are then installed.",
            action='store_true',
            dest='use_pythonpath',
            default=False)

        parser.add_option(
            '--site-packages',
            dest='no_site_packages',
            action='store_false',
            help="Setup the virtual environment to use the global site-packages",
            default=True)

        parser.add_option('--config',
            help='Use an INI config file to specify the packages used in this installation.  Using this option clears the initial configuration, but multiple uses of this option will add package specifications.',
            action='append',
            dest='config_files',
            default=[])

        parser.add_option('--keep-config',
            help='Keep the initial configuration data that was specified if the --config option is specified.',
            action='store_true',
            dest='keep_config',
            default=False)

        parser.add_option('--localize',
            help='Force localization of DOS scripts on Linux platforms',
            action='store_true',
            dest='localize',
            default=False)

        #
        # Change the virtualenv options
        #
        parser.get_option("--python").help = "Specify the Python interpreter to use, e.g., --python=python2.5 will install with the python2.5 interpreter."
        parser.remove_option("--relocatable")
        parser.remove_option("--version")
        parser.remove_option("--unzip-setuptools")
        parser.remove_option("--no-site-packages")
        parser.remove_option("--clear")
        #
        # Add description 
        #
        parser.description=self.description
        parser.epilog="If DEST_DIR is not specified, then a default installation path is used:  "+self.default_windir+" on Windows and "+self.default_unixdir+" on Linux.  This command uses the Python 'setuptools' package to install Python packages.  This package installs packages by downloading files from the internet.  If you are running this from within a firewall, you may need to set the HTTP_PROXY environment variable to a value like 'http://<proxyhost>:<port>'."
        

    def adjust_options(self, options, args):
        #
        # Force options.clear to be False.  This allows us to preserve the logic
        # associated with --clear, which we may want to use later.
        #
        options.clear=False
        #
        global vpy_main
        if options.debug:
            vpy_main.raise_exceptions=True
        #
        global logger
        verbosity = options.verbose - options.quiet
        self.logger = Logger([(Logger.level_for_integer(2-verbosity), sys.stdout)])
        logger = self.logger
        #
        if options.update and (options.stable or options.trunk):
            self.logger.fatal("ERROR: cannot specify --stable or --trunk when specifying the --update option.")
            sys.exit(1000)
        if options.update and len(options.config_files) > 0:
            self.logger.fatal("ERROR: cannot specify --config when specifying the --update option.")
            sys.exit(1000)
        if options.update and options.keep_config:
            self.logger.fatal("ERROR: cannot specify --keep-config when specifying the --update option.")
            sys.exit(1000)
        if len(args) > 1:
            self.logger.fatal("ERROR: installer script can only have one argument")
            sys.exit(1000)
        #
        # Error checking
        #
        if not options.preinstall and (os.path.exists(self.abshome_dir) ^ options.update):
            if options.update:
                self.logger.fatal(wrapper.fill("ERROR: The 'update' option is specified, but the installation path '%s' does not exist!" % self.home_dir))
                sys.exit(1000)
            elif os.path.exists(join(self.abshome_dir,'bin')):
                    self.logger.fatal(wrapper.fill("ERROR: The installation path '%s' already exists!  Use the --update option if you wish to update, or remove this directory to create a fresh installation." % self.home_dir))
                    sys.exit(1000)
        if len(args) == 0:
            args.append(self.abshome_dir)
        #
        # Parse config files
        #
        if options.update:
            self.config=None
            options.config_files.append( join(self.abshome_dir, 'admin', 'config.ini') )
        if not self.config is None and (len(options.config_files) == 0 or options.keep_config):
            fp = StringIO.StringIO(self.config)
            self.read_config_file(fp=fp)
            fp.close()
        if not self.config_file is None and (len(options.config_files) == 0 or options.keep_config):
            self.read_config_file(file=self.config_file)
        for file in options.config_files:
            self.read_config_file(file=file)
        print "-----------------------------------------------------------------"
        print "Finished processing configuration information."
        print "-----------------------------------------------------------------"
        print " START - Configuration summary"
        print "-----------------------------------------------------------------"
        self.write_config(stream=sys.stdout)
        print "-----------------------------------------------------------------"
        print " END - Configuration summary"
        print "-----------------------------------------------------------------"
        #
        # If applying preinstall, then only do subversion exports
        #
        if options.preinstall:
            Repository.svn_get='export'

    def get_homedir(self, options, args):
        #
        # Figure out the installation directory
        #
        if len(args) == 0:
            path = self.guess_path()
            if path is None or options.preinstall:
                # Install in a default location.
                if sys.platform == 'win32':
                    home_dir = self.default_windir
                else:
                    home_dir = self.default_unixdir
            else:
                home_dir = os.path.dirname(os.path.dirname(path))
        else:
            home_dir = args[0]
        self.home_dir = home_dir
        self.abshome_dir = os.path.abspath(home_dir)

    def guess_path(self):
        return None

    def setup_installer(self, options):
        if options.preinstall:
            print "Creating preinstall zip file in '%s'" % self.home_dir
        elif options.update:
            print "Updating existing installation in '%s'" % self.home_dir
        else:
            print "Starting fresh installation in '%s'" % self.home_dir
        #
        # Setup HTTP proxy
        #
        if options.offline:
            os.environ['HTTP_PROXY'] = ''
            os.environ['http_proxy'] = ''
        else:
            proxy = ''
            if not options.proxy is None:
                proxy = options.proxy
            if proxy is '':
                proxy = os.environ.get('HTTP_PROXY', '')
            if proxy is '':
                proxy = os.environ.get('http_proxy', '')
            os.environ['HTTP_PROXY'] = proxy
            os.environ['http_proxy'] = proxy
            print "  using the HTTP_PROXY environment: %s" % proxy
            print ""
        #
        # Disable the PYTHONPATH, to isolate this installation from 
        # other Python installations that a user may be working with.
        #
        if not options.use_pythonpath:
            try:
                del os.environ["PYTHONPATH"]
            except:
                pass
        #
        # If --preinstall is declared, then we remove the directory, and prepare a ZIP file
        # that contains the full installation.
        #
        if options.preinstall:
            print "-----------------------------------------------------------------"
            print " STARTING preinstall in directory %s" % self.home_dir
            print "-----------------------------------------------------------------"
            rmtree(self.abshome_dir)
            os.mkdir(self.abshome_dir)
        #
        # When preinstalling or working offline, disable the 
        # default install_setuptools() function.
        #
        if options.preinstall or options.offline:
            install_setuptools.use_default=False
            install_pip.use_default=False
        #
        # If we're clearing the current installation, then remove a bunch of
        # directories
        #
        elif options.clear:
            path = join(self.abshome_dir,'src')
            if os.path.exists(path):
                rmtree(path)
        #
        # Open up zip files
        #
        for file in options.zip:
            unzip_file(file, dir=self.abshome_dir)

        if options.preinstall or not options.offline:
            self.get_packages(options)
        else:
            self.sw_packages.insert( 0, Repository('virtualenv', pypi='virtualenv') )
            self.sw_packages.insert( 0, Repository('pip', pypi='pip') )
            self.sw_packages.insert( 0, Repository('setuptools', pypi='setuptools') )
            #
            # Configure the package versions, for offline installs
            #
            for pkg in self.sw_packages:
                pkg.guess_versions(True)

    def get_packages(self, options):
        #
        # Setup the 'admin' directory
        #
        if not os.path.exists(self.abshome_dir):
            os.mkdir(self.abshome_dir)
        if not os.path.exists(join(self.abshome_dir,'admin')):
            os.mkdir(join(self.abshome_dir,'admin'))
        if options.update:
            INPUT=open(join(self.abshome_dir,'admin',"virtualenv.cfg"),'r')
            options.trunk = INPUT.readline().strip() != 'False'
            options.stable = INPUT.readline().strip() != 'False'
            INPUT.close()
        else:
            OUTPUT=open(join(self.abshome_dir,'admin',"virtualenv.cfg"),'w')
            print >>OUTPUT, options.trunk
            print >>OUTPUT, options.stable
            OUTPUT.close()
            self.write_config( join(self.abshome_dir,'admin','config.ini') )
        #
        # Setup package directories
        #
        if not os.path.exists(join(self.abshome_dir,'dist')):
            os.mkdir(join(self.abshome_dir,'dist'))
        if not os.path.exists(self.abshome_dir+os.sep+"src"):
            os.mkdir(self.abshome_dir+os.sep+"src")
        if not os.path.exists(self.abshome_dir+os.sep+"bin"):
            os.mkdir(self.abshome_dir+os.sep+"bin")
        #
        # Get source packages
        #
        self.sw_packages.insert( 0, Repository('virtualenv', pypi='virtualenv') )
        self.sw_packages.insert( 0, Repository('pip', pypi='pip') )
        if options.preinstall:
            #
            # When preinstalling, add the setuptools package to the installation list
            #
            self.sw_packages.insert( 0, Repository('setuptools', pypi='setuptools') )
        #
        # Add Coopr Forum packages
        #
        self.get_other_packages(options)
        #
        # Get package source
        #
        for pkg in self.sw_packages:
            pkg.guess_versions(False)
            if not pkg.install:
                pkg.find_pkgroot(trunk=options.trunk, stable=options.stable, release=not (options.trunk or options.stable))
                continue
            if pkg.dev:
                tmp = join(self.abshome_dir,'src',pkg.name)
            else:
                tmp = join(self.abshome_dir,'dist',pkg.name)
            if options.trunk:
                if not options.update:
                    pkg.install_trunk(dir=tmp, install=False, preinstall=options.preinstall, offline=options.offline)
            elif options.stable:
                if not options.update:
                    pkg.install_stable(dir=tmp, install=False, preinstall=options.preinstall, offline=options.offline)
            else:
                if not options.update:
                    pkg.install_release(dir=tmp, install=False, preinstall=options.preinstall, offline=options.offline)
        if options.update or not os.path.exists(join(self.abshome_dir,'doc')):
            self.install_auxdirs(options)
        #
        # Create a README.txt file
        #
        OUTPUT=open(join(self.abshome_dir,"README.txt"),"w")
        print >>OUTPUT, self.README.strip()
        OUTPUT.close()
        #
        # Finalize preinstall
        #
        if options.preinstall:
            print "-----------------------------------------------------------------"
            print " FINISHED preinstall in directory %s" % self.home_dir
            print "-----------------------------------------------------------------"
            os.chdir(self.abshome_dir)
            zip_file(self.default_dirname+'.zip', ['.'])
            sys.exit(0)

    def get_other_packages(self, options):
        #
        # Used by subclasses of Installer to 
        # add packages that were requested through other means....
        #
        pass
        
    def install_packages(self, options):
        #
        # Set the bin directory
        #
        if os.path.exists(self.abshome_dir+os.sep+"Scripts"):
            bindir = join(self.abshome_dir,"Scripts")
        else:
            bindir = join(self.abshome_dir,"bin")
        if is_jython:
            Repository.python = os.path.abspath(join(bindir, 'jython.bat'))
        else:
            Repository.python = os.path.abspath(join(bindir, 'python'))
        if os.path.exists(os.path.abspath(join(bindir, 'easy_install'))):
            Repository.easy_install_path = [Repository.python, os.path.abspath(join(bindir, 'easy_install'))]
        else:
            Repository.easy_install_path = [os.path.abspath(join(bindir, 'easy_install.exe'))]
        #
        # Install the related packages
        #
        for pkg in self.sw_packages:
            if not pkg.install:
                pkg.find_pkgroot(trunk=options.trunk, stable=options.stable, release=not (options.trunk or options.stable))
                continue
            if pkg.dev:
                srcdir = join(self.abshome_dir,'src',pkg.name)
            else:
                srcdir = join(self.abshome_dir,'dist',pkg.name)
            if options.trunk:
                if options.update:
                    pkg.update_trunk(dir=srcdir)
                else:
                    pkg.install_trunk(dir=srcdir, preinstall=options.preinstall, offline=options.offline)
            elif options.stable:
                if options.update:
                    pkg.update_stable(dir=srcdir)
                else:
                    pkg.install_stable(dir=srcdir, preinstall=options.preinstall, offline=options.offline)
            else:
                if options.update:
                    pkg.update_release(dir=srcdir)
                else:
                    pkg.install_release(dir=srcdir, preinstall=options.preinstall, offline=options.offline)
        #
        # Copy the <env>/Scripts/* files into <env>/bin
        #
        if os.path.exists(self.abshome_dir+os.sep+"Scripts"):
            for file in glob.glob(self.abshome_dir+os.sep+"Scripts"+os.sep+"*"):
                shutil.copy(file, self.abshome_dir+os.sep+"bin")
        #
        # Localize DOS cmd files
        #
        self.localize_cmd_files(self.abshome_dir, options.localize)
        #
        # Misc notifications
        #
        if not options.update:
            print ""
            print "-----------------------------------------------------------------"
            print "  Add %s to the PATH environment variable" % (self.home_dir+os.sep+"bin")
            print "-----------------------------------------------------------------"
        print ""
        print "Finished installation in '%s'" % self.home_dir

    def localize_cmd_files(self, dir, force_localization=False):
        """
        Hard-code the path to Python that is used in the Python CMD files that
        are installed.
        """
        if not (sys.platform.startswith('win') or force_localization):
            return
        for file in self.cmd_files:
            INPUT = open(join(dir,'bin',file), 'r')
            content = "".join(INPUT.readlines())
            INPUT.close()
            content = content.replace('__VIRTUAL_ENV__',dir)
            OUTPUT = open(join(dir,'bin',file), 'w')
            OUTPUT.write(content)
            OUTPUT.close()

    def svnjoin(*args):
        return '/'.join(args[1:])

    def install_auxdirs(self, options):
        for todir,pkg,fromdir in self.auxdir:
            pkgroot = self.sw_dict[pkg].pkgroot
            if options.update:
                cmd = [Repository.svn,'update','-q',self.svnjoin(self.abshome_dir, todir)]
            else:
                if options.clear:
                    rmtree( join(self.abshome_dir,todir) )
                cmd = [Repository.svn,Repository.svn_get,'-q',self.svnjoin(pkgroot,fromdir),join(self.abshome_dir,todir)]
            print "Running command '%s'" % " ".join(cmd)
            call_subprocess(cmd, filter_stdout=filter_python_develop,show_stdout=True)

    def read_config_file(self, file=None, fp=None):
        """
        Read a config file.
        """
        parser = OrderedConfigParser()
        if not fp is None:
            parser.readfp(fp, '<default configuration>')
        elif not os.path.exists(file):
            if not '/' in file and not self.config_file is None:
                file = os.path.dirname(self.config_file)+"/"+file
            try:
                if sys.version_info[:2] <= (2,5):
                    output = urllib2.urlopen(file).read()
                else:
                    output = urllib2.urlopen(file, timeout=30).read()
            except Exception, err:
                print "Problems opening configuration url:",file
                raise
            fp = StringIO.StringIO(output)
            parser.readfp(fp, file)
            fp.close()
        else:
            if not file in parser.read(file):
                raise IOError, "Error while parsing file %s." % file
        sections = parser.sections()
        if 'installer' in sections:
            for option, value in parser.items('installer'):
                setattr(self, option, apply_template(value, os.environ) )
        if 'localize' in sections:
            for option, value in parser.items('localize'):
                self.add_dos_cmd(option)
        for sec in sections:
            if sec in ['installer', 'localize']:
                continue
            if sec.endswith(':auxdir'):
                auxdir = sec[:-7]
                for option, value in parser.items(sec):
                    self.add_auxdir(auxdir, option, apply_template(value, os.environ) )
            else:
                options = {}
                for option, value in parser.items(sec):
                    options[option] = apply_template(value, os.environ)
                self.add_repository(sec, **options)

    def write_config(self, filename=None, stream=None):
        if not filename is None:
            OUTPUT=open(filename,'w')
            self.write_config(stream=OUTPUT)
            OUTPUT.close()
        else: 
            for repos in self.sw_packages:
                repos.write_config(stream)
                print >>stream, ""
            if len(self.cmd_files) > 0:
                print >>stream, "[localize]"
                for file in self.cmd_files:
                    print >>stream, file+"="
                print >>stream, "\n"
        


def configure(installer):
    """
    A dummy configuration function.
    """
    return installer

def create_installer():
    return Installer()

def get_installer():
    """
    Return an instance of the installer object.  If this object
    does not already exist, then create the object and use the
    configure() function to customize it based on the end-user's
    needs.

    The argument to this function is the class type that will be
    constructed if needed.
    """
    try:
        return get_installer.installer
    except:
        get_installer.installer = configure( create_installer() )
        return get_installer.installer
    

#
# Override the default definition of rmtree, to better handle MSWindows errors
# that are associated with read-only files
#
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def rmtree(dir):
    if os.path.exists(dir):
        logger.notify('Deleting tree %s', dir)
        shutil.rmtree(dir, ignore_errors=False, onerror=handleRemoveReadonly)
    else:
        logger.info('Do not need to delete %s; already gone', dir)

#
# This is a monkey patch, to add control for exception management.
#
vpy_main = main
vpy_main.raise_exceptions=False
def main():
    if sys.platform != 'win32':
        if os.environ.get('TMPDIR','') == '.':
            os.environ['TMPDIR'] = '/tmp'
        elif os.environ.get('TEMPDIR','') == '.':
            os.environ['TEMPDIR'] = '/tmp'
    try:
        vpy_main()
    except Exception, err:
        if vpy_main.raise_exceptions:
            raise
        print ""
        print "ERROR:",str(err)

#
# This is a monkey patch, to control the execution of the install_setuptools()
# function that is defined by virtualenv.
#
default_install_setuptools = install_setuptools

def install_setuptools(py_executable, unzip=False):
    try:
        if install_setuptools.use_default:
            default_install_setuptools(py_executable, unzip)
    except OSError, err:
        print "-----------------------------------------------------------------"
        print "Error installing the 'setuptools' package!"
        if os.environ['HTTP_PROXY'] == '':
            print ""
            print "WARNING: you may need to set your HTTP_PROXY environment variable!"
        print "-----------------------------------------------------------------"
        sys.exit(0)

install_setuptools.use_default=True


#
# This is a monkey patch, to control the execution of the install_pip()
# function that is defined by virtualenv.
#
default_install_pip = install_pip

def install_pip(*args, **kwds):
    try:
        if install_pip.use_default:
            default_install_pip(*args, **kwds)
    except OSError, err:
        print "-----------------------------------------------------------------"
        print "Error installing the 'pip' package!"
        if os.environ['HTTP_PROXY'] == '':
            print ""
            print "WARNING: you may need to set your HTTP_PROXY environment variable!"
        print "-----------------------------------------------------------------"
        sys.exit(0)

install_pip.use_default=True


#
# The following methods will be called by virtualenv
#
def extend_parser(parser):
    installer = get_installer()
    installer.modify_parser(parser)

def adjust_options(options, args):
    installer = get_installer()
    installer.get_homedir(options, args)
    installer.adjust_options(options, args)
    installer.setup_installer(options)
    
def after_install(options, home_dir):
    installer = get_installer()
    installer.install_packages(options)

