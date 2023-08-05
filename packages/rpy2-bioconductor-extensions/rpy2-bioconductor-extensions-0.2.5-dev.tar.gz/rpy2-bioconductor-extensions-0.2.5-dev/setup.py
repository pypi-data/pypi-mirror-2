from distutils.core import setup


version = __import__('bioc').__version__

packages = ('bioc', )

setup(
    name = 'rpy2-bioconductor-extensions',
    version = version,
    description = "Bioconductor-specific extensions for rpy2",
    long_description = """rpy2.bioconductor-extensions proposes extensions to rpy2 for bioconductor/bioinformatics users""", 
    author = 'Laurent Gautier',
    author_email = 'lgautier@gmail.com',
    url = 'no url yet',
    license = 'GPLv3',
    platforms = ['any'],
    package_dir = {'bioc': 'bioc'},
    packages = packages,
    classifiers = ['Development Status :: 1 - Planning',
                   'Programming Language :: Python',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'Operating System :: OS Independent'],
)


