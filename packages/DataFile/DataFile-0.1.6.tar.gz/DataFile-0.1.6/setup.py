from distutils.core import setup

setup(
    name='DataFile' ,
    version='0.1.6' ,
    author='JMA',
    author_email='jeanmichel.arbona@gmail.com',
    packages=['datafile','datafile.test'],
    license='LICENSE.txt',
    classifiers=["Programming Language :: Python",
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                "Operating System :: OS Independent",
                "Development Status :: 2 - Pre-Alpha",
                "Topic :: Scientific/Engineering"],
    description='Easy way to read data files',
    long_description=open('README.txt').read(),
    )
