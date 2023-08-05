# This setup.py was generated automatically by Pyron.
# For details, see http://pypi.python.org/pypi/pyron/

from setuptools import setup, find_packages

setup(
    name = 'cursive.pymag',
    version = '0.3',
    description = u'Author tools for Python Magazine',
    long_description = u"\nPython Magazine uses a special markup language, called Ceres, for\nformatting articles that are submitted by authors and then worked on by\nour editorial crew.  So that we can support Python folks who want to\nwrite their documents in `reStructured Text`_ instead, this package adds\na ``pymag`` sub-command to the ``cursive`` command-line tool that\nconverts an article to Ceres, and while doing so reports any problems\nwith the article that might interfere with the magazine's layout.\n\nTo use the command, just type something like this::\n\n    $ cursive pymag my_article.rst\n\nThis package builds on the features of `cursive.tools`_.\n\n.. _reStructured Text: http://docutils.sourceforge.net/rst.html\n.. _cursive.tools: http://pypi.python.org/pypi/cursive.tools/\n",
    author = 'Brandon Craig Rhodes',
    author_email = 'brandon@rhodesmill.org',
    url = 'http://bitbucket.org/brandon/cursivepymag/',
    classifiers = ['Development Status :: 5 - Production/Stable', 'License :: OSI Approved :: MIT License', 'Topic :: Text Processing', 'Topic :: Text Processing :: Markup'],

    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    install_requires = ['cursive.tools'],
    entry_points = '[cursive.commands]\npymag = cursive.pymag.format:command\n',
    )
