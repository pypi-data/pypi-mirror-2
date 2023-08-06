====================
"Cloud" sphinx theme
====================

About
=====
:mod:`cloud_sptheme` provides a theme called "Cloud", used to generate this documentation.
Aside from being another sphinx theme, it has a few special features:

* You can mark sections with ``.. rst-class:: html-toggle``,
  which will make the section default to being collapsed under html,
  with a "show section" toggle link to the right of the title.

* It adds some addtional css classes to the base sphinx layout,
  allowing more options for custom styling.

* It provides configuration options allowing the relbar's title to
  point to a page other than the table of contents,
  allowing easy separation table-of-contents and front pages
  (such as used by this documentation).

List of Options
===============

``externalrefs``
    whether references should be displayed differently

``externalicon``
    optional image or string to prefix before any external links.

``roottarget``
    sets the page which the title link in the relbar should point to.
    defaults to ``"<toc>"``, the table of contents.

``logotarget``
    sets the page which the sidebar logo (if any) should point to.
    defaults to ``<root>``, which mirrors ``roottarget``.

``docwidth``
    set the maximum document width, so the manual does not stretch
    too far on wide monitors. defaults to ``12in``.

``docheight``
    sets the minimum height of the page body. defaults to ``6in``.

See ``cloud_sptheme/themes/cloud/theme.conf`` for a complete list of options.

Usage
=====
To use the cloud theme, open your documentation's ``conf.py`` file, make the following changes::

    # import Cloud
    import cloud_sptheme as csp

    #... contents omitted...

    #set the html theme
    html_theme = "cloud"

    #... contents omitted...

    #set the theme path to point to cloud's theme data
    html_theme_path = [csp.get_theme_dir()]

Additionaly you will probably want to set some of the theme options listed above.
