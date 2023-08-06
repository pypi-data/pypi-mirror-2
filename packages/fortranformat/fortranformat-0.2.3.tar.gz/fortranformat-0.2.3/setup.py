from distutils.core import setup

setup(
    name = 'fortranformat',
    packages = ['fortranformat'],
    version = '0.2.3',
    description = 'Mimics Fortran textual IO in Python',
    author = 'Brendan Arnold',
    author_email = 'brendanarnold@gmail.com',
    url = 'http://bitbucket.org/brendanarnold/py-fortranformat',
    download_url = 'https://bitbucket.org/brendanarnold/py-fortranformat/downloads/fortranformat-0.2.3.tar.gz',
    keywords = ['fortran', 'io', 'interface', 'format'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Fortran',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Scientific/Engineering',
    ],
    long_description = '''
    FORTRAN format interpreter for Python
    -------------------------------------    

    Generates text from some Python variables or will read a line of
    text into Python variables according to the format statement passed

    
'''
)
