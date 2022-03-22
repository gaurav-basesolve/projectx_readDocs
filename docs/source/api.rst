Api
===

Save Access
-----------

Configuring projectx tool action runs this function, ``cli.base.save_access()``, behind the scene.

.. autofunction:: cli.base.save_access


Check Access
------------

Action that shows current configure of projectx runs ``cli.base.check_access()`` function:

.. autofunction:: cli.base.check_access

Copying files
--------------

To copy files from aws, you can use the ``cli.base.aws_cp()`` function:

.. autofunction:: cli.base.aws_cp

Major part of functions uses *projectx_service* class described under :ref:`Call out <callOut>` section when checking user access or running different action like getting all *sample_id*.

.. _callOut:

Call out
--------

.. autoclass:: cli.service.projectx_service
