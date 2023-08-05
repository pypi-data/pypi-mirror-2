# This setup.py was generated automatically by Pyron.
# For details, see http://pypi.python.org/pypi/pyron/

from setuptools import setup, find_packages

setup(
    name = 'cursive.pymag',
    version = '1.0',
    description = u'Author tools for Python Magazine',
    long_description = u"\nPython Magazine uses a special markup language, called Ceres, for\nformatting articles that are submitted by authors and then worked on by\nour editorial crew.  So that we can support Python folks who want to\nwrite their documents in `reStructured Text`_ instead, this package adds\na ``pymag`` sub-command to the ``cursive`` command-line tool that\nconverts an article to Ceres, and while doing so reports any problems\nwith the article that might interfere with the magazine's layout.\n\nTo use the command, just type something like this::\n\n    $ cursive pymag my_article.rst\n\nThanks to Doug Hellmann, there is also now a tool to go the other\ndirection, from Ceres to RST: the ``ceres2rst`` sub-command will take a\ntypical ``page.src.txt`` file and produce an RST equivalent.  Invoke it\nlike this::\n\n    $ cursive ceres2rst page.src.txt\n\nReport any bugs to the `project page`_ on Bitbucket.  This package builds\non the features of `cursive.tools`_.\n\n.. _reStructured Text: http://docutils.sourceforge.net/rst.html\n.. _project page: http://pypi.python.org/pypi/cursive.pymag/\n.. _cursive.tools: http://pypi.python.org/pypi/cursive.tools/\n",
    author = 'Brandon Craig Rhodes',
    author_email = 'brandon@rhodesmill.org',
    url = 'http://bitbucket.org/brandon/cursivepymag/',
    classifiers = ['Development Status :: 5 - Production/Stable', 'License :: OSI Approved :: MIT License', 'Topic :: Text Processing', 'Topic :: Text Processing :: Markup'],

    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    install_requires = ['cursive.tools'],
    entry_points = '[cursive.commands]\npymag = cursive.pymag.format:command\nceres2rst = cursive.pymag.torst:command\n',
    )
