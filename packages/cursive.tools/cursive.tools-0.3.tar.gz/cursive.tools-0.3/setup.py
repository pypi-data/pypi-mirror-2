# This setup.py was generated automatically by Pyron.
# For details, see http://pypi.python.org/pypi/pyron/

from setuptools import setup, find_packages

setup(
    name = 'cursive.tools',
    version = '0.3',
    description = u'Tools for authoring restructured text files',
    long_description = u'\nThis package provides a ``cursive`` command that is intended to become\nthe core of a whole set of tools for working with `reStructured Text`_\ndocuments.  The command supports sub-commands, some of which come\nbuilt-in with this package, and others that become available as other\ncursive modules are installed.\n\nThe single built-in command available at this point is:\n\n``cursive wc <filename>``\n    Word count: ignoring headers, code snippets, and comments, this\n    routine figures out the number of words in your document, and prints\n    out a total both for each section of your document separately and\n    also for the document as a whole.\n\nThe other module currently available to supplement cursive is the\n`cursive.pymag`_ package, which will format an article for publication\nin Python Magazine.\n\n.. _reStructured Text: http://docutils.sourceforge.net/rst.html\n.. _cursive.pymag: http://pypi.python.org/pypi/cursive.pymag/\n',
    author = 'Brandon Craig Rhodes',
    author_email = 'brandon@rhodesmill.org',
    url = 'http://bitbucket.org/brandon/cursivetools/',
    classifiers = ['Development Status :: 5 - Production/Stable', 'License :: OSI Approved :: MIT License', 'Topic :: Text Processing', 'Topic :: Text Processing :: Markup'],

    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    install_requires = ['docutils'],
    entry_points = '[console_scripts]\ncursive = cursive.tools.cursive:console_script_cursive\n\n[cursive.commands]\nwc = cursive.tools.wc:command\n',
    )
