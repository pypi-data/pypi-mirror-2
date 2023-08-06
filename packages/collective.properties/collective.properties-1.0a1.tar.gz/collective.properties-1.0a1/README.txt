Introduction
============

Provides form to update object properties via ``Plone`` UI.


Quick Intro
-----------

* it replicates ZMI ``/manage_propertiesForm`` form in ``Plone`` UI
* it's like ``collective.interfaces`` package to manage zope interfaces via
  ``Plone`` but to manage ``PropertyManager`` based properties
* it uses ``z3c.form`` library to generate CRUD form
* it is tested in ``Plone 3`` (``Plone 4`` to be checked soon)
* it's installable via ``portal quickinstaller`` tool, for detailed instructions
  on how to add it to your zope instance, please, check ``docs/INSTALL.txt``
  file


Property attributes
-------------------

``IPropertyManager`` interface provides properties with the next list of
metadata:

* ``id``: required
* ``type``: required
* ``select_variable``: optional; for selection and multiple selection property
  types to provide the name of a property or method which returns a list of
  strings from which the selection(s) can be chosen
* ``mode``: optional; must contain 0 or more chars from the set 'w', 'd'; 'w' -
  value may be changed by user, 'd' - user can delete property, '' - property
  and it's value may be shown in property listings, but it is read-only and
  may not be deleted; without mode key property is assumed to have the mode 'wd'
  (writeable and deletable)
* ``label``: optional
* ``description``: optional


Property types
--------------

Default property manager property types are listed below. All of them are
planned to be supported by ``collective.properties`` management form (see
``TODO`` section below for what's not implemented yet):

* ``float``
* ``int``
* ``long``
* ``string``
* ``lines``
* ``text``
* ``date``
* ``tokens``
* ``selection``
* ``multiple selection``


Notes
-----

``Property Manager`` interface defines some reserved strings that are prohibited
to be used as property ids. It provides validation method which is also used by
collective.properties management form. That's why it's secure to install this
package in ``Plone`` site and let non-tech content manager use it's properties
form.

Not all standard properties are handled yet. For details, please, see ``TODO``
section below.

``collective.properties`` form simply skips property types that it doesn't
know how to handle. So to manage them you still need to use standard
``/manage_propertiesForm`` form.
