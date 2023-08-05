Introduction
============

collective.tabr allows for easy editing of "tabbed content" using the `jQuery
Tools Tabs`_ UI tool.

Installation
------------

Add collective.tabr to your buildout. It uses the z3c.autoinclude plugin so you
do not need to add it to the ``zcml=`` section of your buildout.

Install via the Add-on Products control panel like you would any other Product.

Usage
-----

Tabs are created by selecting "Tab" from the style menu of your editor. This
will cause everything after the "Tab" element to be a part of that tab's pane
until another Tab, Default Tab, or "Pane Break" is reached. For example::

  <h2 class="content-tab">First Tab</h2>
  <p>This is a paragraph inside the first tab</p>
  
  <h2 class="default-content-tab">Second Tab</h2>
  <p>This is a paragraph inside the second tab</p>
  <p>This tab will be shown first</p>
  
  <hr class="pane-break" />
  
  <p>This paragraph is not inside of a tab</p>
  
  <h2 class="content-tab">First Tab part 2</h2>
  <p>This paragraph will be in the first tab of the second grouping of tabs</p>
  
This will result in two groups of tabs, the first of which will contain two tabs
of which the second will be pre-selected when the page loads. The second tab
group will only have a single tab in it, and it will be preceded by a paragraph
between itself and the end of the previous tab group.

Customizing
-----------

CSS is available in the ``tabr`` skin layer for customization, as are the 
example images for the CSS.


Dependencies
------------

This package depends on the `jQuery Tools`_ library which is provided by
`plone.app.jquerytools`_. It does not depend on a specific version of either
jQuery Tools or jQuery, but you should check to make sure that another package
is not including multiple versions of any library in use, though this is not
common.


.. _`jQuery Tools`: http://flowplayer.org/tools/index.html
.. _`jQuery Tools Tabs`: http://flowplayer.org/tools/tabs/index.html
.. _`plone.app.jquerytools`: http://pypi.python.org/pypi/plone.app.jquerytools

Credits
=======

Thanks to Mikko Ohtamaa for `collective.kuputabs`_ which was my inspiration for
this. Most of the code was his to begin with, and I ripped it appart and made
*many* changes.

Also thanks to Douglas Bowman for his `CSS Sliding Doors`_ technique for the
tab styling.

.. _`collective.kuputabs`: http://pypi.python.org/pypi/collective.kuputabs
.. _`CSS Sliding Doors`: http://www.alistapart.com/articles/slidingdoors2/

