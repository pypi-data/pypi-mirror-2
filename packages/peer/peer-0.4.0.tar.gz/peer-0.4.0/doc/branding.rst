
Branding customization guidelines
=================================

Mision
-------

The look&feel of the PEER website,  will be adaptable to differents worldwide services that will come up.

To assure a global identification underneath to all of the future design themes, we are envolving PEER style guidelines as a reference point for all designers creating a PEER website.

We have made a basic guides difference between *things to change* and  *locked things*.

Locked guides
-------------
Page layout & content placement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The page width is 1024px but the content is limited to 960px width.
Indeed there´s main page division, leaving a 242px right side column in content block. This right column will appear on multiple site´s views and will always show content related actions.

We have also employed an 17px baseline grid to help with vertical alignment of page components. 
Firm adherence to the baseline isn’t necessary for all typography but it does help to create vertical rhythm on the page.

Blocks height and width values, on the page layout will be locked for the future PEER themes.

.. image:: generic_layout.png


Things to change
----------------
Background colors and images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Header, content and footer background are free to apply any style change on their background color and image properties. 
Actually they could be different from each other, given as a result, a new creative site look&feel.

.. image:: bg_styles.png

Font styles
^^^^^^^^^^^
Headings, links, and body text styles are wholly free to change in any of their style properties.

In this guides group must to be mentioned, the home banner, that obviously, is free to change completly its image and slogan.

.. image:: font_styles.png

jQuery UI theme
^^^^^^^^^^^^^^^
The global identification will be support by the use of a jQuery custom theme. 
It would be apply in any site button, icon, user messages... and spread all over the web site.

You can create and download your own jQuery custom theme in the `Theme Roller application
<http://jqueryui.com/themeroller/>`_.

It must to be the 1.8.14 theme version Stable, for jQuery 1.3.2+

How to change styles
--------------------

The customizable theme options can be achieved by changing the settings.py file located in the project´s main directory.

The options to change are located in this file´s block:

::

 PEER_THEME = {
    'LINK_COLOR': '#5669CE',
    'LINK_HOVER': '#1631BC',
    'HEADING_COLOR': '#1631BC',
    'INDEX_HEADING_COLOR': '#ff7b33',
    'HEADER_BACKGROUND': '',
    'CONTENT_BACKGROUND': '',
    'FOOTER_BACKGROUND': '',
    'HOME_TITLE': 'Nice to meet you!!',
    'HOME_SUBTITLE': 'Say hello to federated worldwide services',
    'JQUERY_UI_THEME': 'default-theme',
 }
