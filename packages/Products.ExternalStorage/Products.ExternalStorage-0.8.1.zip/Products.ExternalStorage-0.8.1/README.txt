About
=====

    ``ExternalStorage`` is a storage for Archetypes storing the fields contents
    outside the ZODB. So it works in a fashion like ExternalFile or similar
    products.


.. Warning::

    ``ExternalStorage`` is not actively maintained anymore.  For new Plone
    3.x sites or higher, please have a look at `plone.app.blob`_.

.. _`plone.app.blob`: http://pypi.python.org/pypi/plone.app.blob


.. Note::

    ``ExternalStorage`` 0.6 *requires* an Archetypes version *after* 1.3.3-final.
    Older Archetypes versions have critical bugs and won't work with this
    version of ExternalStorage.

Usage
-----

    Simply define one of your field's storages in a schema as ExternalStorage.
    (see ExternalExample in examples/).

Example
-------

    Copy examples/ExternalExample into your Products dir.

Defining Custom Path Policy
---------------------------

    You can provide your own path policy, just write a method on your
    class called 'getExternalPath' (or anything else that you specified
    at 'path_method' when intantiating the storage).

    Some common uses include:

    1) Instance relative path to current portal (default):
       path = portal_url.getRelativeContentURL(instance)

    2) Instance absolute path, including portal name and all above
       path = '/'.join(instance.getPhysicalPath())

    3) Flat Instance UID
       path = instance(UID())

    4) Sorted by Portal Type
       path = instance.getTypeInfo().getId() + '/' + instance.getId()

    By default, files are stored accordingly policy (1). If class has
    multiple fields, then (1) will be a folder and the files are stored
    inside it, following the field names.

    Remember to provide additional code to support multiple fields
    when providing your custom path policy.

Archive
-------

    In some previous versions there was some sort of archive support.
    This was implemented as a copy of the old content in some special
    folder.

    It's removed from the current version, but will be readded later.

