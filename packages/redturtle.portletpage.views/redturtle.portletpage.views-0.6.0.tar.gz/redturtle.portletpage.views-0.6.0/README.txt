Introduction
============

Some additional views for the great `collective.portletpage`__ product.

__ http://pypi.python.org/pypi/collective.portletpage

After installing this, while still having the default "*Two columns*" view, you can also rely on:

 `Just portlets`
     Show only the portlets section, hiding *Title* and *RichText* body.
 `No title`
     Show all sections, not the *Title*.
 `Tabbed regions`
     Show portlet columns with tabs, using Plone standard tabbed layout.

When using the *Tabbed regions* view, you can see 1 to 4 tabs, taken from the portletpage columns
(empty columns are not show).

Default label for tabs is "*Section x*" where *x* is the column number. You can customize labels adding a
new property (only through ZMI for now) to the Portlet Page content calling it "**tab_labels**"
(type *lines*) and adding to it **4 values** that are used to be tab labels in order.

Labels provided are translated using "*plone*" domain so you can provide i18n support in your themes or
products for the values you put inside the property.

Requirements
============

* Tested with collective.portletpage 1.0b3
* Tested with Plone 3.2 and 3.3


