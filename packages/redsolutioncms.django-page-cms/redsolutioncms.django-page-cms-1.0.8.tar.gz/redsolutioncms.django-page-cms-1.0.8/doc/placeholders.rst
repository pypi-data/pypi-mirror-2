=========================
Placeholders template tag
=========================

The syntax for placeholder is the following::

    {% placeholder <name> [on <page>] [with <widget>] [parsed] [as <varname>] %}

A few explanations are needed:

* If the **on** option is not specified the CMS will automatically
  take the current page (by using the `current_page` context variable)
  to get the content of the placeholder.

* If the **widget** option is not specified the CMS will render a simple `TextInput`.

* If you use the keyword **parsed** the content of the placeholder
  will be evaluated as Django template, within the current context.

* Each placeholder with the **parsed** keyword defined will also have
  a note in the admin interface noting its ability to be evaluated as template.

* If you use the option **as** you will define in the template's context
  with the content of the placeholder that you will be able to use for different purpose.

To clarify, here is a list of different possible syntaxes for this template tag::

    {% placeholder title %}
    {% placeholder title with TextIntput %}
    {% placeholder body with Textarea %}
    {% placeholder right-column on another_page_object %}
    
    {% placeholder body parsed %}
    {% placeholder right-column as right_column %}

    ..random content..

    <div class="my_funky_column">{{ right_column|safe }}</div>

List of placeholder widgets
===========================

Placeholder could be rendered with different widgets

TextInput
---------

A simple line input::

    {% placeholder [name] with TextInput %}

Textarea
--------

A multi line input::

    {% placeholder [name] with Textarea %}

RichTextarea
------------

A simple `Rich Text Area Editor <http://batiste.dosimple.ch/blog/posts/2007-09-11-1/rich-text-editor-jquery.html>`_ based on jQuery::

    {% placeholder [name] with RichTextarea %}

.. image:: http://rte-light.googlecode.com/svn/trunk/screenshot.png

WYMEditor
---------

A complete jQuery Rich Text Editor called `wymeditor <http://www.wymeditor.org/>`_::

    {% placeholder [name] with WYMEditor %}

.. image:: http://drupal.org/files/images/wymeditor.preview.jpg

markItUpMarkdown
----------------

markdown editor based on `markitup <http://markitup.jaysalvat.com/home/>`_::

    {% placeholder [name] with markItUpMarkdown %}

.. image:: http://www.webdesignerdepot.com/wp-content/uploads/2008/11/05_markitup.jpg

markItUpHTML
------------

A HTML editor based on `markitup <http://markitup.jaysalvat.com/home/>`_::

    {% placeholder [name] with markItUpHTML %}

.. image:: http://t37.net/files/markitup-081127.jpg

TinyMCE
-------

HTML editor based on `TinyMCE <http://tinymce.moxiecode.com/>`_

1. You should install the `django-tinymce <http://pypi.python.org/pypi/django-tinymce/1.5>`_ application first
2. Then in your settings you should activate the application::

    PAGE_TINYMCE = True

3. And add ``tinymce`` in your ``INSTALLED_APPS`` list.

The basic javascript files required to run TinyMCE are distributed with this CMS.

However if you want to use plugins you need to fully install TinyMCE.
To do that follow carefully `those install instructions <http://code.google.com/p/django-tinymce/source/browse/trunk/docs/installation.rst>`_

Usage::

    {% placeholder [name] with TinyMCE %}

.. image:: http://mgccl.com/gallery2/g2data/albums/2006/11/tinymce.png

EditArea
--------

Allows to edit raw html code with syntax highlight based on [http://www.cdolivet.com/index.php?page=editArea editArea]

The code (Javascript, CSS) for editarea is not included into the codebase.
To get the code you can add this into your svn external dependecies::

    pages/media/pages/edit_area -r29 https://editarea.svn.sourceforge.net/svnroot/editarea/trunk/edit_area

Usage::

    {% placeholder [name] with EditArea %}

.. image:: http://sourceforge.net/dbimage.php?id=69125&image.png