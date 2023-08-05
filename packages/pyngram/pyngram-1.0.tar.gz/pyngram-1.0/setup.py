from distutils.core import setup

classifiers = [ 'Topic :: Scientific/Engineering :: Bio-Informatics',
                'Topic :: Security :: Cryptography',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Text Processing',
                'Topic :: Text Processing :: General',
                'Topic :: Text Processing :: Linguistic',
                'Topic :: Utilities',
                ]

setup(
    name = 'pyngram',
    license = 'MIT',
    author = 'Jay Liew',
    author_email = 'twitter.com/jaysern',
    version = '1.0',
    url = 'http://jayliew.com',
    description = 'A simple Python n-gram calculator',
    long_description = open('README.txt').read(),
    keywords = ['ngram', 'n-gram', 'bigram', 'digram', 'trigram', 'substitution', 
                'cipher', 'crackme', 'crypto', 'caesar', 'decodeme'],
    classifiers = classifiers,
    py_modules = ['pyngram',],
    )
