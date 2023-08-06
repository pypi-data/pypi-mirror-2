NAME
----

    zkaffold

DESCRIPTION
-----------

    A plone product to install content on a plone site.

FEATURES
--------

    * Install content
    * Install products
    * Delete content
    * Apply zope interfaces
    * Modify content
    * Generate test content

HOW TO INSTALL
--------------

    Add zkaffold to your product:

      * Add "zkaffold" to your product's install_requires in setup.py
      * Add <include package="zkaffold" /> in your product's configure.zcml
      * Add "profile-zkaffold:default" as a dependency to your product's
        metadata.xml
      * run ./bin/buildout

    Zkaffold should now be installed.  Note that zkaffold is not installable /
    uninstallable from the portal quick installer.

HOW TO USE
----------

    After installing zkaffold in your plone site, you can build content for
    your plone site by:

      * create "initial" profile in your product,
      * create a directory called "zkaffold" in profile/initial,
      * create structure.xml (example structure.xml is in
        zkaffold/exportimport/tests/test_exportimport.py),

    You can also create default users in your plone site by:

      * create members.xml (example members.xml is in
        zkaffold/exportimport/tests/test_exportimport.py)

    If you are using buildout, in your buildout.cfg:

      * in the [plonesite] section, add your product initial profile (e.g.
        mysite:initial) to "profiles-initial",
      * run ./bin/buildout

    Your plone site should now be populated with content specified in
    structure.xml.  Note that if your plone site already exists before running
    buildout, it will not add any content.  You'll have to delete your plone
    site or run the zkaffold import step to add the content.

    You can use different profiles to create different content, for example if
    you want test content, you can create another profile and add that in
    profiles-initial when you want test content to be built.

    Zkaffold publishes all objects by default by trying to apply transition
    "publish" to the objects.  If your objects need a different way of
    publishing, have a look at
    zkaffold/exportimport/tests/test_exportimport.py.

DEPENDENCIES
------------

    zkaffold depends on lxml, which depends on libxml2-dev and libxslt-dev.
    In Debian, you can use:

      * sudo aptitude install libxml2-dev libxslt-dev

PLUGIN
------

    zkaffold supports a plugin system for exporting content:

      * Add an import step for your profile initial,
      * create an exporter for your field, it should return a
        lxml.etree.Element for <param> or (lxml.etree.Element for <param>,
        filename, file content)::

            def my_field_exporter(plone_object, field):
                ...
                return param

      * create the import step to register the field exporter::

            from zkaffold.contextexporter import IContentExporter

            def register_field_exporters(context):
                portal = context.getSite()
                sm = portal.getSiteManager()
                exporter = sm.getUtility(IContentExporter)
                exporter.register_field_exporter('mysite.fields.MyField',
                        'mysite.field_exporters.my_field_exporter')

TESTS
-----

    To run zkaffold's tests, you need to:

      * add "zkaffold [test]" in the "eggs" in the [test] section of your
        buildout.cfg,
      * run ./bin/buildout,
      * ./bin/test
