import os, sys

from distutils.core import setup, Extension
import distutils.sysconfig

try:
    import sphinx
except:
    sphinx = None

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PyTango'))

from release import Release

BOOST_ROOT = OMNI_ROOT = TANGO_ROOT = NUMPY_ROOT = '/usr'

TANGO_ROOT = os.environ.get('TANGO_ROOT', TANGO_ROOT)
OMNI_ROOT  = os.environ.get('OMNI_ROOT', OMNI_ROOT)
BOOST_ROOT = os.environ.get('BOOST_ROOT', BOOST_ROOT)
NUMPY_ROOT = os.environ.get('NUMPY_ROOT', NUMPY_ROOT)

# if there is no numpy then for sure disable usage of it in PyTango

numpy_capi_available = os.path.isdir(os.path.join(NUMPY_ROOT, 'include','numpy'))

numpy_available = False
try:
    import numpy
    numpy_available = True
except Exception, e:
    pass

print '-- Compilation information --------------------------------------------'
print 'Build %s %s' % (Release.name, Release.version)
print 'Using Python %s' % distutils.sysconfig.get_python_version()
print '\tinclude: %s' % distutils.sysconfig.get_python_inc()
print '\tlibrary: %s' % distutils.sysconfig.get_python_lib()
print 'Using omniORB from %s' % OMNI_ROOT
print 'Using Tango from %s' % TANGO_ROOT
print 'Using boost python from %s' % BOOST_ROOT
if numpy_available:
    if numpy_capi_available:
        print 'Using numpy %s' % numpy.version.version
        print '\tinclude: %s' % os.path.join(NUMPY_ROOT, 'include','numpy')
    else:
        print 'NOT using numpy (numpy available but C source is not)'
else:
    print 'NOT using numpy (it is not available)'
print '-----------------------------------------------------------------------'

author = (Release.authors['Coutinho'], Release.authors['Sune'])

please_debug = False

packages = [
    'PyTango',
    'PyTango3'
]

provides = [
    'PyTango',
    'PyTango3'
]

requires = [
]

package_data = {
    'PyTango' : []
}

data_files = []

classifiers = [
    'Development Status :: %s revision %s' % (Release.version, '1'),
    'Environment :: Library',
    'Intended Audience :: Developers',
    'License :: %s' % Release.license,
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Tango :: Python :: PyTango',
]

def uniquify(seq):
    no_dups = []
    [ no_dups.append(i) for i in seq if not no_dups.count(i) ]
    return no_dups

include_dirs = [
    os.path.abspath('src'),
    os.path.join(TANGO_ROOT, 'include'),
    os.path.join(OMNI_ROOT, 'include'),
    os.path.join(NUMPY_ROOT, 'include'),
]

libraries = [
        'tango',
        'log4tango',
    ]

extra_compile_args = []

extra_link_args = []

macros = []

if not numpy_available or not numpy_capi_available:
    macros.append( ('DISABLE_PYTANGO_NUMPY', None) )

if os.name == 'nt':
    include_dirs += [ BOOST_ROOT ]

    if please_debug:
        libraries += [
            #'libboost_python-vc80-mt-1_38', Boost in windows autodetects the proper library to link itself with...
            'omniORB414d_rt',
            'omniDynamic414d_rt',
            'omnithread34d_rt',
            'COS414d_rt',
        ]
        extra_compile_args += []
        extra_link_args += ['/DEBUG']
        macros += [ ('_DEBUG', None) ]
    else:
        libraries += [
            #'libboost_python-vc80-mt-1_38', Boost in windows autodetects the proper library to link itself with...
            'omniORB414_rt',
            'omniDynamic414_rt',
            'omnithread34_rt',
            'COS414_rt',
        ]


    extra_compile_args += [
        '/EHsc'
    ]

    extra_link_args += []

    macros += [
        #('_WINDOWS', None),
        #('_USRDLL', None),
        #('_TANGO_LIB', None),
        #('JPG_USE_ASM', None),
        ('LOG4TANGO_HAS_DLL', None),
        ('TANGO_HAS_DLL', None),
        ('WIN32', None),
    ]

else:
    if please_debug:
        extra_compile_args += ['-g', '-O0']
        extra_link_args += ['-g' , '-O0']
    
    include_dirs += [ os.path.join(BOOST_ROOT, 'include') ]
    libraries += [
        'boost_python',
        'pthread',
        'rt',
        'dl',
        'omniORB4',
        'omniDynamic4',
        'omnithread',
        'COS4',
    ]

    extra_compile_args += []

    extra_link_args += [
        '-Wl,-h',
        '-Wl,--strip-all',
    ]

    macros += []

include_dirs = uniquify(include_dirs)

library_dirs = [
    os.path.join(TANGO_ROOT, 'lib'),
    os.path.join(OMNI_ROOT, 'lib', 'x86_win32'),
    os.path.join(BOOST_ROOT, 'lib'),
]
library_dirs = uniquify(library_dirs)


_cppfiles_exclude = []
_cppfiles  = [ os.path.join('src',fname) for fname in os.listdir('src') if fname.endswith('.cpp') and not fname in _cppfiles_exclude]
_cppfiles += [ os.path.join('src','server',fname) for fname in os.listdir(os.path.join('src','server')) if fname.endswith('.cpp') and not fname in _cppfiles_exclude]

_pytango = Extension(name               = '_PyTango',
                     sources            = _cppfiles,
                     include_dirs       = include_dirs,
                     library_dirs       = library_dirs,
                     libraries          = libraries,
                     define_macros      = macros,
                     extra_compile_args = extra_compile_args,
                     extra_link_args    = extra_link_args,
                     language           = 'c++'
                     )

from distutils.core import Command

class build_doc(Command):

    description = "\"build\" sphinx documentation (copy to build directory)"

    user_options = [
        ('build-lib=', 'd', "directory to \"build\" (copy) to"),
        ('build-temp=', 't', "temporary build directory"),
        ('doc-fmt=', None, "documentation format (html/dirhtml/helphtml/latex/text). Default is html"),
        ('force', 'f', "forcibly build everything (ignore file timestamps)"),
    ]

    def initialize_options (self):
        self.build_lib = None
        self.build_temp = None
        self.doc_fmt = None
        self.force = 0

    def finalize_options (self):
        self.set_undefined_options('build',
                                   ('build_lib', 'build_lib'),
                                   ('build_temp', 'build_temp'),
                                   ('doc_fmt', 'doc_fmt'),
                                   ('force', 'force'))

    def run (self):
        if sphinx is None:
            print "Sphinx is not available. Documentation will not be generated"
            return

        build_dir = os.path.join(self.build_lib, 'doc', self.doc_fmt)
        build_dir = os.path.join('build_doc', self.doc_fmt)
        build_temp = os.path.join(self.build_temp, 'doc')
        
        #make sure the documentation is using the recently compiled PyTango
        sys.path = [os.path.abspath(self.build_lib)] + sys.path

        opts  = ['sphinx-build']
        if self.force:
            opts += ['-a', '-E']
        opts += ['-d', build_temp]
        opts += ['-b', self.doc_fmt]
        opts += ['./doc', build_dir]
        ret = sphinx.main(opts)

from distutils.command.build import build as dftbuild

class build(dftbuild):

    user_options = dftbuild.user_options + \
        [('doc-fmt=', None, "documentation format (html/dirhtml/helphtml/latex/text). Default is html")]

    def initialize_options (self):
        dftbuild.initialize_options(self)
        self.doc_fmt = 'html'

    def finalize_options (self):
        dftbuild.finalize_options(self)

    def has_doc(self):
        return os.path.isdir('doc')

    sub_commands = dftbuild.sub_commands + [('build_doc', has_doc)]

setup(name          = 'PyTango',
      version       = Release.version,
      description   = Release.description,
      author        = author[0][0] + ' & ' + author[1][0],
      author_email  = author[0][1] + ' & ' + author[1][1],
      url           = Release.url,
      download_url  = Release.download_url,
      packages      = packages,
      package_dir   = { 'PyTango' : 'PyTango', 'PyTango3' : 'PyTango3' },
      classifiers   = classifiers,
      package_data  = package_data,
      data_files    = data_files,
      provides      = provides,
      keywords      = Release.keywords,
      requires      = requires,
      ext_package   = 'PyTango',
      ext_modules   = [_pytango],
      cmdclass      = { 'build' : build,
                        'build_doc' : build_doc })
