# coding=utf-8
from distutils.core import setup

files = ["text_hr/.suff_registry.pickle"]

setup(
    name='text-hr',
    version='0.10',
    #Name the folder where your packages live:
    packages = ['text_hr'],
    #'package' package must contain files (see list above)
    #It says, package *needs* these files.
    package_data = {'text_hr' : files },
    description = "Morphological/Inflection Engine for Croatian language, POS tagger, stopwords",
    author = "Robert Lujo",
    author_email = "trebor74hr@gmail.com",
    url = "http://bitbucket.org/trebor74hr/text-hr/",
    #'runner' is in the root.
    # scripts = ["runner"],
    long_description = """
    Morphological/Inflection Engine for Croatian language
    =====================================================

    Includes stopwords and Part-Of-Speech tagging engine (POS tagging) based on
    inverse inflection algorithm for detection. 
    
    TAGS
    ----
    Croatian language, python, natural language processing (NLP), 
    Part-of-speech (POS) tagging, stopwords, inverse inflection. 
    
    OZNAKE
    ------
    Hrvatski jezik, Python biblioteka, morfologija,
    infleksija, obrnuta infleksija, prepoznavanje vrsta rijeci, 
    racunalna obrada govornog jezika, zaustavne rijeci.

    Installation
    ============
    Installation instructions:
    - download zip
    - unzip
    - open shell
    - go to distribution directory
    - python setup.py install
    
    Usage
    =====
    Usage example - start python shell::

        > python 
        >>> import text_hr
        >>> ...

    """,
    # TODO: enable hr chars in char before

    # This next part it for the Cheese Shop
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Croatian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: Indexing',
      ]
    )


