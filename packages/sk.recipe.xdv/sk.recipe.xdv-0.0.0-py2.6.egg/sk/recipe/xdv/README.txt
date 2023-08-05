Supported Options
=================

The ``sk.recipe.xdv`` recipe supports the following options:

``rules``
    (Required.) The rules XML file to compile.
``theme``
    (Required.) The theme HTML file to use as a template.
``output``
    (Optional.) Where to write the XSLT file as a result of compilation.
    If not given, the recipe will create a subdirectory in the Buildout's
    ``parts`` directory named after the part in the buildout
    configuration, and will create the compiled XSLT in that directory
    named ``theme.xsl``.
``includemode``
    (Optional.) Tells how to de-reference content included by the rules,
    defaults to ``document``.  In ``document`` mode, included content is
    inserted via the XSLT ``document()`` function.  In ``ssi`` mode, it's
    by server-side include (and requires a compatible webserver).  In
    ``esi`` mode, it's by edge-side include (and requires a compatible
    cache server).
``network``
    (Optional.) Tells if it's OK to access the network in order to resolve
    entities (fetch resources); specify either ``true`` or ``false``.
    Defaults to false if the Buildout itself is running in offline mode.

If you don't specify the ``output`` option, then this recipe sets it to the
path of the generated theme XSLT file.  You can then use that value in other
parts of the buildout with ``${part-name:output}`` where ``part-name`` is the
name of the part that used the ``sk.recipe.xdv`` recipe.


Example Usage
=============

For this demonstration, we have pre-prepared rules and template files named
``rules.xml`` and ``theme.html`` in the ``testdata`` subdirectory.  Let's grab
some convenient references to these files::

    >>> import os.path
    >>> testdata = join(os.path.dirname(__file__), 'testdata')
    >>> rulesXML = join(testdata, 'rules.xml')
    >>> themeHTML = join(testdata, 'theme.html')

Now let's make a buildout that compiles those rules and theme template::

    >>> write(sample_buildout, 'buildout.cfg', '''
    ... [buildout]
    ... parts = my-rules
    ...
    ... [my-rules]
    ... recipe = sk.recipe.xdv
    ... rules = %(rules)s
    ... theme = %(theme)s
    ... ''' % dict(rules=rulesXML, theme=themeHTML))

We list the two required settings, ``rules`` and ``theme``, and let Buildout
do its thing::

    >>> print system(buildout)
    Installing my-rules.

Since we left every other option at the defaults, the recipe compiled the
rules and template theme into a file named ``theme.xsl`` and stuck it in a
subdirectory of the Buildout's parts directory named ``my-rules``, which
you'll notice is the name of the part in the ``buildout.cfg`` file::

    >>> ls('parts', 'my-rules')
    -  theme.xsl

What's it look like?  Let's check::

    >>> cat('parts', 'my-rules', 'theme.xsl') # doctest: +ELLIPSIS
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"...

That looks like XSLT to me.


Controlling the Destination File
--------------------------------

The default behavior of writing the compiled XSLT output to the parts
directory makes sense for most Buildout situations, but you may want further
control.  Let's update the ``buildout.cfg`` file to do just that::

    >>> destDir = tmpdir('my-dir')
    >>> destXSL = join(destDir, 'my-output.xsl')
    >>> write(sample_buildout, 'buildout.cfg', '''
    ... [buildout]
    ... parts = my-rules
    ...
    ... [my-rules]
    ... recipe = sk.recipe.xdv
    ... output = %(destination)s
    ... rules = %(rules)s
    ... theme = %(theme)s
    ... ''' % dict(destination=destXSL, rules=rulesXML, theme=themeHTML))

Re-running the Buildout::

    >>> print system(buildout)
    Uninstalling my-rules.
    Installing my-rules.

And now look what showed up in our working directory::

    >>> ls(destDir)
    -  my-output.xsl
    
Perfect.


Controlling 3rd-Party Entity Inclusion
--------------------------------------

XDV normally generates XSLT that translates content from an underlying
production system into the desired theme by applying the rules.  However,
content can also come from 3rd-party resources that are not part of the
current resource stream.  If you don't tell in the rules file how to retrieve
them, then a default resource method will be used.  You can specify what that
default method should be using the ``includemode`` option.

Unless otherwise stated, the include mode uses the XSLT ``document`` function.
You can be explicit about that by stating ``document`` in the recipe's part::

    [my-rules]
    recipe = sk.recipe.xdv
    includemode = document
    ...
    
Other include modes are ``ssi`` to use server-side includes and ``esi`` to use
edge-side includes.  Let's give one of these a try.  First, let's update the
``buildout.cfg``:

    >>> destDir = tmpdir('another-dir')
    >>> docBased = join(destDir, 'doc-based.xsl')
    >>> ssiBased = join(destDir, 'ssi-based.xsl')
    >>> write(sample_buildout, 'buildout.cfg', '''
    ... [buildout]
    ... parts =
    ...     doc-based
    ...     ssi-based
    ...
    ... [doc-based]
    ... recipe = sk.recipe.xdv
    ... includemode = document
    ... output = %(docBased)s
    ... rules = %(rules)s
    ... theme = %(theme)s
    ...
    ... [ssi-based]
    ... recipe = sk.recipe.xdv
    ... includemode = ssi
    ... output = %(ssiBased)s
    ... rules = %(rules)s
    ... theme = %(theme)s
    ... ''' % dict(docBased=docBased, ssiBased=ssiBased, rules=rulesXML, theme=themeHTML))

Now let's run the Buildout and see how the output differs::

    >>> print system(buildout)
    Uninstalling my-rules.
    Installing doc-based.
    Installing ssi-based.

And now look what showed up in our working directory::

    >>> ls(destDir)
    -  doc-based.xsl
    -  ssi-based.xsl
    >>> cat(docBased) # doctest: +ELLIPSIS
    <xsl:stylesheet ...<xsl:copy-of select="document('/legal.html', .)//*[@id = ...
    >>> cat(ssiBased) # doctest: +ELLIPSIS
    <xsl:stylesheet ... <xsl:copy-of select="/html/head/div[2]"/><xsl:comment># include  virtual="/legal.html...

ESI works similarly (if it really works at all; testing it this morning gives
me errors from the XDV compiler).
