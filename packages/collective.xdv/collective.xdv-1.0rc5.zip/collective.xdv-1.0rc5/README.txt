============
Introduction
============

This package offers a simple way to develop and deploy Plone themes using
the `XDV`_ engine. If you are not familiar with XDV or rules-based theming,
check out the `XDV documentation <http://pypi.python.org/pypi/xdv>`_.

.. contents:: Contents

Installation
============

collective.xdv depends on:

  * `plone.transformchain`_ to hook the transformation into the publisher
  * `plone.registry`_ and `plone.app.registry`_ to manage settings
  * `plone.autoform`_, `plone.z3cform`_ and `plone.app.z3cform`_ to render the 
    control panel
  * `five.globalrequest`_ and `zope.globalrequest`_ for internal request
    access
  * `XDV`_, containing XDV itself itself
  * `lxml`_ to perform the final transform

These will all be pulled in automatically if you are using zc.buildout and
follow the installation instructions.

To install collective.xdv into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor. Locate the section that looks like this::

    # extends = http://dist.plone.org/release/3.3/versions.cfg
    extends = versions.cfg
    versions = versions

It may also have a URL in the "extends" section, similar to the commented-out
first line, depending on whether you pull the Plone configuration from the
network or locally.

To add collective.xdv to our setup, we need some slightly different versions
of a couple of the packages, so we extend the base config with a version list
from the good-py service, so change this part of the configuration so it looks
like this::

    extends =
        versions.cfg
        http://good-py.appspot.com/release/collective.xdv/1.0
    versions = versions

Note that the last part of the URL above is a version number. There may be
a newer version by the time you read this, so check out the `overview
page <http://good-py.appspot.com/release/collective.xdv>`_ for the known good
set.

What happens here is that the dependency list for collective.xdv specifies
some new versions for you via the good-py URL. This way, you don't have to
worry about getting the right versions, Buildout will handle it for you.

Next step is to add the actual collective.xdv add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the collective.xdv on a separate line, like this::

    eggs =
        Plone
        collective.xdv [Zope2.10]

Note the use of the [Zope2.10] extra, which brings in the
ZPublisherEventsBackport package for forward compatibility with Zope 2.12 /
Plone 4. If you are using Zope 2.12 or later (e.g. with Plone 4), you should
do::

    eggs =
        Plone
        collective.xdv

Note that there is no need to add a ZCML slug as collective.xdv uses
z3c.autoinclude to configure itself automatically.

Once you have added these lines to your configuration file, it's time to run
buildout, so the system can add and set up collective.xdv for you. Go to the
command line, and from the root of your Plone instance (same directory as
buildout.cfg is located in), run buildout like this::

    $ bin/buildout

You will see output similar to this::

    Getting distribution for 'collective.xdv==1.0'.
    Got collective.xdv 1.0.
    Getting distribution for 'plone.app.registry'.
    Got plone.app.registry 1.0a1.
    Getting distribution for 'plone.synchronize'.
    Got plone.synchronize 1.0b1.
    ...

If everything went according to plan, you now have collective.xdv installed
in your Zope instance.

Next, start up Zope, e.g with::

    $ bin/instance fg

Then go to the "Add-ons" control panel in Plone as an administrator, and
install the "XDV theme support" product. You should then notice a new
"XDV Theme" control panel in Plone's site setup.
    
Usage
=====

In the "XDV Theme" control panel, you can set the following options:

  Enabled yes/no
    Whether or not the transform is enabled.

  Domains
    A list of domains (including ports) that will be matched against
    the HOST header to determine if the theme should be applied. Note that
    127.0.0.1 is never styled, to ensure there's always a way back into Plone
    to change these very settings. However, 'localhost' should work just fine.
  
  Theme
    A file path or URL pointing to the theme file. This is just a
    static HTML file.

  Rules
    The filesystem path to the rules XML file.  
  
  Alternate themes
    A list of definitions of alternate themes and rules files for a different path.
    Should be of the form 'path|theme|rules' where path may use a regular expression 
    syntax, theme is a file path or URL to the theme template and
    rule is a file path to the rules file.
  
  XSLT extension file
    It is possible to extend XDV with a custom XSLT file. If you have such
    a file, give its URL here.
    
  Absolute prefix
    If given, any relative URL in an ``<img />``, ``<link />``, ``<style />``
    or ``<script />`` in the theme HTML file will be prefixed by this URL
    snippet when the theme is compiled. This makes it easier to develop theme
    HTML/CSS on the file system using relative paths that still work on any
    URL on the server.
    
  Unstyled paths
    This is used to give a list of URL patterns (using regular
    expression syntax) for pages that will not be styled even if XDV is
    enabled. By default, this includes the 'emptypage' view that is necessary
    for the Kupu editor to work, and the manage_* pages that make up the
    ZMI.
    
Note that when Zope is in debug mode, the theme will be re-compiled on each
request. In non-debug mode, it is compiled once on startup, and then only
if the control panel values are changed.

Resources in Python packages
----------------------------

When specifying the rules, theme and/or XSLT extension files, you should
normally use a file path. If you are distributing your theme in a Python
package that is installed using Distribute/setuptools (e.g. a standard
Plone package installed via buildout), you can use the special ``python``
URL scheme to reference your files.

For example, if your package is called ``my.package`` and it contains a
directory ``mytheme``, you could reference the file ``rules.xml`` in that
file as::

    ``python://my.package/mytheme/rules.xml``

This will be resolved to an absolute ``file://`` URL by the collective.xdv.

Static files and CSS
--------------------

Typically, the theme will reference static resources such as images or
stylesheets. It is usually a good idea to keep all of these in a single,
top-level directory to minimise the risk of clashes with Plone content paths.

If you are using Zope/Plone standalone, you will need to make your static
resources available through Zope, or serve them from a separate (sub-)domain.
Here, you have a few options:

 * Create the static resources as ``File`` content objects through Plone.
 * Create the resources inside the ``portal_skins/custom`` folder in the ZMI.
 * Install the resources through a filesystem product.

The latter is most the appropriate option if you are distributing your theme
as a Python package. In this case, you can register a resource directory in
ZCML like so::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">
        
        ...
        
        <browser:resourceDirectory
            name="my.package"
            directory="mytheme"
            />
        
        ...

    </configure>

The ``mytheme`` directory should be in the same directory as the
``configure.zcml`` file. You can now put your theme, rules and static
resources here.

If you make sure that your theme uses only relative URLs to reference any
stylesheets, JavaScript files, or images that it needs (including those
referenced from stylesheets), you should now be able to view your static
theme by going to a URL like::

    http://localhost:8080/Plone/++resource++my.package/theme.html

You can now set the "Absolute prefix" configuration option to be
'/++resource++my.package'. XDV will then turn those relative URLs into
appropriate absolute URLs with this prefix.

If you have put Apache, nginx or IIS in front of Zope, you may want to serve
the static resources from the web server directly instead.

Using portal_css to manage your CSS
-----------------------------------

Plone's "resource registries", including the ``portal_css`` tool, can be used
to manage CSS stylesheets. This offers several advantages over simply linking
to your stylesheets in the template, such as:

* Detailed control over the ordering of stylesheets
* Merging of stylesheets to reduce the number of downloads required to render
  your page
* On-the-fly stylesheet compression (e.g. whitespace removal)
* The ability to include or exclude a stylesheet based on an expression

It is usually desirable (and sometimes completely necessary) to leave the
theme file untouched, but you can still use ``portal_css`` to manage your
stylesheets. The trick is to drop the theme's styles and then include all
styles from Plone. For example, you could add the following rules::

    <drop theme="/html/head/link" />
    <drop theme="/html/head/style" />
    
    <!-- Pull in Plone CSS -->
    <append theme="/html/head" content="/html/head/link | /html/head/style" />

The use of an "or" expression for the content in the ``<append />`` rule means
that the precise ordering is maintained.

For an example of how to register stylesheets upon product installation using
GenericSetup, see below. In short - use the ``cssregistry.xml`` import step
in your GenericSetup profile directory.

There is one important caveat, however. Your stylesheet may include relative
URL references of the following form:

    background-image: url(../images/bg.jpg);
    
If your stylesheet lives in a resource directory (e.g. it is registered in
``portal_css`` with the id ``++resource++my.package/css/styles.css``), this
will work fine so long as the registry (and Zope) is in debug mode. The
relative URL will be resolved by the browser to
``++resource++my.package/images/bg.jpg``.

However, you may find that the relative URL breaks when the registry is put
into production mode. This is because resource merging also changes the URL
of the stylesheet to be something like::

    /plone-site/portal_css/Suburst+Theme/merged-cachekey-1234.css

To correct for this, you have a few options:

1. Replace your static stylesheet with something dynamic so that you can
   calculate it relative an absolute path on the fly. This obviously will not
   work if you want to be able to view the theme standalone.
2. Change your URLs to use an absolute path, e.g.
   ``/++resource++my.theme/images/bg.jpg``. Again, this will break the
   original stylesheet. However, you can perhaps create a Plone-only override
   stylesheet that overrides each CSS property that uses a url().
3. Avoid using ``portal_css`` for your static stylesheets.
4. Use Plone 4. :-) In Plone 4 (b3 and later), the ``portal_css`` tool has an
   option to parse a stylesheet for relative URLs and apply an absolute prefix
   based on the stylesheet's debug-mode URL. The option is called
   ``applyPrefix`` in the ``cssregistry.xml`` syntax.

Controlling Plone's default CSS
-------------------------------

It is sometimes useful to show some of Plone's CSS in the styled site. You
can achieve this by using an XDV ``<append />`` rule or similar to copy the
CSS from Plone's generated ``<head />`` into the theme. You can use the
portal_css tool to turn off the style sheets you do not want.

However, if you also want the site to be usable in non-themed mode (e.g. on
a separate URL), you may want to have a larger set of styles enabled when
XDV is not used. To make this easier, you can use the following expressions
as conditions in the portal_css tool (and portal_javascripts, portal_kss),
in portal_actions, in page templates, and other places that use TAL expression
syntax::

    request/HTTP_X_XDV | nothing

This expression will return True if XDV is currently enabled, in which case
an HTTP header "X-XDV" will be set. By default, this will check both the
'enabled' flag in the XDV control panel, and the current domain. If you later
deploy the theme to a fronting web server such as nginx, you can set the
same request header there to get the same effect, even if collective.xdv is
uninstalled.

Use::

    not: request/HTTP_X_XDV | nothing
    
to 'hide' a style sheet from the themed site.

A worked example
=================

There are many ways to set up an XDV theme. For example, you could upload
the theme and rules as content in Plone use absolute paths to configure them.
You could also serve them from a separate static web server, or even load
them from the filesystem.

To create a deployable theme, however, it is often best to create a simple
Python package. This also provides a natural home for theme-related 
customisations such as template overrides.

Although a detailed tutorial is beyond the scope of this help file, a brief,
worked example is shown below.

1. Create a package and install it in your buildout::

    $ cd src
    $ paster create -t plone my.theme

See `the buildout manual`_ for details

If you have a recent ``ZopeSkel`` installed, this should work. Pick ``easy``
mode. Answer "yes" when asked if you want to register a profile.

Then edit ``buildout.cfg`` to add your new package (``my.theme`` above) to the
``develop`` and ``eggs`` lists.

2. Edit ``setup.py`` inside the newly created package

The ``install_requires`` list should be::

    install_requires=[
          'setuptools',
          'collective.xdv',
      ],

Re-run buildout::

    $ bin/buildout

3. Edit ``configure.zcml`` inside the newly created package.

Add a resource directory inside the ``<configure />`` tag. Note that you may
need to add the ``browser`` namespace, as shown.

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        i18n_domain="my.theme">

        <genericsetup:registerProfile
            name="default"
            title="my.theme"
            directory="profiles/default"
            description="Installs the my.theme package"
            provides="Products.GenericSetup.interfaces.EXTENSION"
            />

        <browser:resourceDirectory
            name="my.theme"
            directory="static"
            />
  
    </configure>

Here, we have used the package name, ``my.theme``, for the resource directory
name. Adjust as appropriate.

4. Add a ``static`` directory next to ``configure.zcml``.

5. Put your theme and rules files into this directory.

For example, you may have a ``theme.html`` that references images in a
sub-directory ``images/`` and stylesheets in a sub-directory ``css/``. Place
this file and the two directories inside the newly created ``static``
directory.

Make sure the theme uses relative URLs (e.g. ``<img src="images/foo.jpg" />``)
to reference its resources. This means you can open theme up from the
filesystem and view it in its splendour.

Also place a ``rules.xml`` file there. See the `XDV`_ documentation for
details about its syntax. You can start with some very simple rules if
you just want to test::

    <?xml version="1.0" encoding="UTF-8"?>
    <rules
        xmlns="http://namespaces.plone.org/xdv"
        xmlns:css="http://namespaces.plone.org/xdv+css">
        
        <!-- Head: title -->
        <replace theme="/html/head/title" content="/html/head/title" />
    
        <!-- Base tag -->
        <replace theme="/html/head/base" content="/html/head/base" />
    
        <!-- Drop styles in the head - these are added back by including them from Plone -->
        <drop theme="/html/head/link" />
        <drop theme="/html/head/style" />
    
        <!-- Pull in Plone CSS -->
        <append theme="/html/head" content="/html/head/link | /html/head/style " />

    </rules>

These rules will pull in the ``<title />`` tag (i.e. the browser window's
title), the ``<base />`` tag (necessary for certain Plone URLs to work
correctly), and Plone's stylesheets.

See below for some more useful rules.

6. Create the installation profile

The generated code above for the ``<genericsetup:registerProfile />`` tag
contains a reference to a directory ``profiles/default``. You may need to
create this next to ``configure.zcml`` if it doesn't exist already, i.e.
create a new directory ``profiles`` and inside it another directory
``default``.

In this directory, add a file called ``metadata.xml`` containing::

    <metadata>
        <version>1</version>
        <dependencies>
            <dependency>profile-collective.xdv:default</dependency>
        </dependencies>
    </metadata>

This will install collective.xdv into Plone when my.theme is installed via
the add-on control panel later.

Also create a file called ``registry.xml``, with the following contents::

    <registry>
    
        <!-- collective.xdv settings -->
        <record interface="collective.xdv.interfaces.ITransformSettings" field="rules">
            <value>python://my.theme/static/rules.xml</value>
        </record>
    
        <record interface="collective.xdv.interfaces.ITransformSettings" field="theme">
            <value>python://my.theme/static/theme.html</value>
        </record>
    
        <record interface="collective.xdv.interfaces.ITransformSettings" field="absolute_prefix">
            <value>/++resource++my.theme</value>
        </record>

    </registry>

Replace ``my.theme`` with your own package name, and ``rules.xml`` and
``theme.html`` as appropriate.

This file configures the settings behind the XDV control panel.

Hint: If you have played with the control panel and want to export your
settings, you can create a snapshot in the ``portal_setup`` tool in the ZMI.
Examine the ``registry.xml`` file this creates, and pick out the records that
relate to ``collective.xdv``. You should strip out the ``<field />`` tags
in the export, so that you are left with ``<record />`` and ``<value />`` tags
as shown above.

Also, add a ``cssregistry.xml`` in the ``profiles/default`` directory to
configure the ``portal_css`` tool::

    <?xml version="1.0"?>
    <object name="portal_css">
 
     <!-- Set conditions on stylesheets we don't want to pull in -->
     <stylesheet
         expression="not:request/HTTP_X_XDV | nothing"
         id="public.css"
         />
     
     <!-- Add new stylesheets -->
     <!-- Note: applyPrefix is not available in Plone < 4.0b3 -->
 
     <stylesheet title="" authenticated="False" cacheable="True"
        compression="safe" conditionalcomment="" cookable="True" enabled="on"
        expression="request/HTTP_X_XDV | nothing"
        id="++resource++my.theme/css/styles.css" media="" rel="stylesheet"
        rendering="link"
        applyPrefix="True"
        />

    </object>

This shows how to set a condition on an existing stylesheet, as well as
registering a brand new one. We've set ``applyPrefix`` to True here, as
explained above. This will only work in Plone 4.b3 and later. For earlier
versions, simply take this out. 

7. Test

Start up Zope and go to your Plone site. Your new package should show as
installable in the add-on product control panel. When installed, it should
install collective.xdv as a dependency and pre-configure it to use your theme
and rule set. By default, the theme is not enabled, so you will need to go to
the control panel to switch it on.

You can now compare your untouched theme, the unstyled Plone site, and the
themed site by using the following URLs:

* ``http://localhost:8080`` (or whatever you have configured as the styled
  domain) for a styled Plone. If you used the sample rule above, this will
  look almost exactly like your theme, but with the ``<title />`` tag
  (normally shown in the title bar of your web browser) taken from Plone.
* ``http://127.0.0.1:8080`` (presuming this is the port where Plone is
  running) for an unstyled Plone.
* ``http://localhost:8080/++resource++my.theme/theme.html`` for the pristine
  theme. This is served as a static resource, almost as if it is being
  opened on the filesystem.

Common rules
============

To copy the page title::

    <!-- Head: title -->
    <replace theme="/html/head/title" content="/html/head/title" />

To copy the ``<base />`` tag (necessary for Plone's links to work)::

    <!-- Base tag -->
    <replace theme="/html/head/base" content="/html/head/base" />

To drop all styles and JavaScript resources from the theme and copy them
from Plone's ``portal_css`` tool instead::

    <!-- Drop styles in the head - these are added back by including them from Plone -->
    <drop theme="/html/head/link" />
    <drop theme="/html/head/style" />
    
    <!-- Pull in Plone CSS -->
    <append theme="/html/head" content="/html/head/link | /html/head/style" />

To copy Plone's JavaScript resources::

    <!-- Pull in Plone CSS -->
    <append theme="/html/head" content="/html/head/script" />

To copy the class of the ``<body />`` tag (necessary for certain Plone
JavaScript functions and styles to work properly)::

    <!-- Body -->
    <prepend theme="/html/body" content="/html/body/attribute::class" />    

Other tips
==========

* Firebug is an excellent tool for inspecting the theme and content when
  building rules. It even has an XPath extractor.
* Read up on XPath. It's not as complex as it looks and very powerful.
* Run Zope in debug mode whilst developing so that you don't need to restart
  to see changes to theme, rules or, resources.

.. _XDV: http://pypi.python.org/pypi/xdv
.. _Deliverance: http://pypi.python.org/pypi/Deliverance
.. _plone.transformchain: http://pypi.python.org/pypi/plone.transformchain
.. _repoze.zope2: http://pypi.python.org/pypi/repoze.zope2
.. _plone.transformchain: http://pypi.python.org/pypi/plone.transformchain
.. _plone.registry: http://pypi.python.org/pypi/plone.registry
.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry
.. _plone.autoform: http://pypi.python.org/pypi/plone.autoform
.. _plone.z3cform: http://pypi.python.org/pypi/plone.z3cform
.. _plone.app.z3cform: http://pypi.python.org/pypi/plone.app.z3cform
.. _lxml: http://pypi.python.org/pypi/lxml
.. _five.globalrequest: http://pypi.python.org/pypi/five.globalrequest
.. _zope.globalrequest: http://pypi.python.org/pypi/zope.globalrequest
.. _the buildout manual: http://plone.org/documentation/manual/developer-manual/managing-projects-with-buildout
