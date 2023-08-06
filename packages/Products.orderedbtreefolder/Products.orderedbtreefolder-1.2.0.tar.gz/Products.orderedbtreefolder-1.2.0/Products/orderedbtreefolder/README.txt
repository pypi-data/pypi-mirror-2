=====================
 Ordered BTreeFolder
=====================

This btree folder class implements the OrderSupport interface from the
core Zope2.7+ distribution. It is a subclass of the BTreeFolder2
product from Shane Hathaway. The BTreeFolder2 product needs to be
installed alongside this product.


Features
========

This folder has the advantages of a normal BTreefolder. Object
listing and access to single objects, does not load unused objects
into memory.

With the ordering support one can use this folder as a base class for
other more application oriented containers.

Every OBTreeFolder has the property ``insertmodus`` which defines
where in the ordering new objects should be added. Default is at the
beginning of the ordered list.

In the ZMI, there is a simple javascript based method to change the
order of several objects with one request.


License
=======

This product is licensed under the GPL, read LICENSE.GPL for more
info.


Info
====

For questions regarding this product you can send an email to

  core@unioncms.org


Contributions
=============

Thanks to Helge Tesdal for a nice optimization hint.
