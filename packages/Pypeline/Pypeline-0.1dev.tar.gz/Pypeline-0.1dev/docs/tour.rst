=========================
Getting to Know Pypeline
=========================

A Brief History
----------------

There are a wide variety of plain text-based syntaxes for generating
documentation, including HTML. GitHub's markup_ library provides a way to handle
all of these formats in an easily-extensible manner. Pypeline provides the same
functionality in a native Python library.

Installing Pypeline
--------------------

In order to install Pypeline, you simply use setuptools/Distribute's
`easy_install` command.  (We recommend using a virtualenv_ for development.)

::

    $ virtualenv pypeline_env
    $ source pypeline_env/bin/activate
    (pypeline_env)$ easy_install -UZ pypeline

Getting Started
----------------

Out of the box Pypeline supports the following markups:

* Markdown
* Textile
* ReST
* Creole
* Plain text

To get started with these::

    >>> from pypeline.markup import markup
    >>> markup.render('foo.txt')
    
Rendering Content
------------------

The render function accepts two parameters: a file path and content. Content is
optional; if no content is provided Pypeline will attempt a basic read() on the
provided file path.

Passing in just the file path::

    >>> markup.render('bar.txt')

Reading in the file is handy when you need more control over the read operation
or need to massage the content before handing it off to Pypeline. For example,
you may want to limit the size of the file being read::

    >>> filepath = '/var/tmp/hello.txt'
    >>> with open(filepath, 'r') as f:
    >>>     content = f.read(65536)
    >>> markup.render(filepath, content)

Extending Pypeline
-------------------

A quick review from the Getting Started section::

    >>> from pypeline.markup import markup
    >>> markup.render('foo.txt')

The markup attribute is an instance of the Markup class with the built-in
markups ready to go. To load your own markups, initialize a new instance::

    >>> from pypeline.markup import Markup
    >>> from bar import my_markups
    >>> markup = Markup(my_markups)
    >>> markup.render('foo.rst')

You can also load your own alongside the built-in markups::

    >>> from pypeline import markups
    >>> markup = Markup(markups, my_markups)
    >>> markup.render('foo.rst')

Defining a Markup
------------------

Your markups can either be a single function or a module. If you use a module,
Pypeline will look for any module functions that end with "_markup" and load each
as an individual markup. A markup function must return a tuple of two things:

1. the pattern used to match supported file extensions
2. a function that takes in a single string parameter and renders it to HTML

Markdown is a good example::

    def markdown_markup():
        import markdown
        return (r'md|mkdn?|mdown|markdown', lambda s: markdown.markdown(s, safe_mode="escape"))

As you can see, the pattern matches a variety of Markdown extensions. Using
Python's support for lambda functions lets us make the render function a
one-liner.

You can also define a more complex render function, for example one that uses a
command line tool to generate the HTML.

Testing Markups
----------------

To test a markup, create a README.format input file (containing whatever markup
you want to test) and a README.format.html output file. Place the files in a
markups directory alongside your test module. Finally you need to modify your
test class to extend TestMarkup::

    >>> from pypeline.tests.test_markup import TestMarkup
    >>> class TestMyMarkup(TestMarkup):

TestMarkup will take care of finding the input files, using your Markups to
generate HTML output, and then comparing the actual output to the expected in
your output file.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _markup: http://github.com/github/markup/
