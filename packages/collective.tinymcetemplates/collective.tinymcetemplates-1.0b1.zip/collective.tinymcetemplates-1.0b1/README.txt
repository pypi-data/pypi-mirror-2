Introduction
============

``collective.tinymcetemplates`` is a Plone 3 add-on that provides a TinyMCE
plugin that allows authors to insert *templates* and *snippets* into the page.

Installation
============

Add ``collective.tinymcetemplates`` to your buildout in the ``eggs`` list, or
as a dependency in the ``install_requires`` list in the ``setup.py`` file
for a product that is already installed in your build. The package's
configuration is loaded automatically by Plone.

You must also install the product in Plone's Add-on control panel.

Usage
=====

Content authors can use the new Template button to insert templates into
the page.

Templates are created and managed as standard Plone Pages:

* The Page title is used as the template title
* The Page description is used as the template description.
* The Page body is used as the the template content.

*Hint:* If you don't want templates to show up in search results, remember
that they need only be accessible to content authors at edit time. You can
thus put them in a workflow state that gives content authors access. You can
also restrict access to templates in this way: an author will not see a
template built from a Page he does not have the permission to see.

To create some templates, the quickest option is to create a Folder with the
id "templates" in the root of the site and put one or more Pages in this
folder.

*Hint:* You can tick the "exclude from navigation" button on the templates
folder to make sure it doesn't show up in the portal tabs or navigation tree.

It's possible to set a different path for templates, and to list multiple
folders. In the configuration registry, as managed by `plone.app.registry`_,
the template paths are listed under the key
``collective.tinymcetemplates.templateLocations``. This contains a tuple of
paths to pages or folders of pages, relative to the portal root. You can
also use GenericSetup to manipulate this list. See `plone.app.registry`_ for
details.

Working with the user's selection
---------------------------------

You can insert the user's current editor selection into your template. To do
this, you need to add a placeholder div or span with the class ``selcontent``.
For example::

    <p>
    You said: <span class="selcontent">(your content here)</span>
    <br />
    We think this is wrong!
    </p>

*Hint:* To insert this class, you can either add it as a paragraph or
character style in the TinyMCE control panel, or insert it into the markup
manually via the HTML view.

When the user now inserts this template into the page, their current selection
will replace the "(your content here)" placeholder.

.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry