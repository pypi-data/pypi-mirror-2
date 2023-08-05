
import sys, shutil
from distutils.core import setup, Extension

# Copy version-specific files
files = {'__init__.py' : 'hyphen/',
        'dictools.py' : 'hyphen/',
        'hnjmodule.c' : 'src/',
        'textwrap2.py' : './',
        'hyphen_config.py' : './'}
ver = sys.version[0]
for file_name, dest in files.items():
    shutil.copy(ver + '.x/' + file_name, dest + file_name)



longdescr = open('README.txt').read()



arg_dict = dict(
    name = "PyHyphen", version = "0.10",
    author = "Dr. Leo",
    author_email = "fhaxbox66@googlemail.com",
    url = "http://pyhyphen.googlecode.com",
    description = "The hyphenation library of OpenOffice and FireFox wrapped for Python",
    long_description = longdescr,
    classifiers = [
        'Intended Audience :: Developers',
         'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: C',
                'Topic :: Text Processing',
                'Topic :: Text Processing :: Linguistic'
    ],
    packages = ['hyphen'],
    ext_modules = [
      Extension('hyphen.hnj', ['src/hnjmodule.c',
                                  'src/hyphen.c',
                                   'src/csutil.c',
                                   'src/hnjalloc.c' ],
                                   include_dirs = ['include'])],
    package_data = {'hyphen':['hyph_en_US.dic']},
    py_modules = ['textwrap2'],
    provides = ['hyphen', 'textwrap2']
)



exec(open('setup-' + ver + '.x.py').read())

