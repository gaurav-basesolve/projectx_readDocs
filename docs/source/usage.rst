Usage
=====


.. _installation:

Installation
------------

Projectx requires `Python`_ v3.8+ to run.

.. _Python: https://www.python.org/

Install the dependencies and open your terminal

**LINUX**

First you need an apikey to have access to our data. A kind of access code. **And** deployment name which will be *DEV*. However this information will be available with the Software-Kit where you get api-key
Use both to configure Projectx.

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx configure
   Enter deployment name> 
   Enter your api_key>

For example

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx configure
   Enter deployment name> DEV
   Enter your api_key: TESTTESTTEST

If it says permission denied, run the following code

.. code-block:: console

    chmod +x pxcli_0.1.0.sif


.. _play:

Play
----

Now as **Projectx** is configured. You can begin playing with it to know more. 

This tool can do many things. We'll go one by one:

1. To get list of analysis that you have access to.

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx list analysis

2. To get names all file that are associated with any analysis

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx list analysis -s <sample-id>

3. To download files associated with any sample-id

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx download -s <sample-id>


By default, a folder "projectx-download" will store files that are downloaded in your systems default Download folder. 
To keep files of different sample-ids together, separate folders will be created and naming of these folder will follow a pattern, i.e., *{patient_name}-{flowcell_id}-{sample_id}-{workflow_name}*,

For example: *Dave-AAJFSK-L8-WES*

**(Optional)** Download a specific file from some sample-id

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx download -s <sample-id> -f <comma-separated list of filename>

**(Optional)** Download files to specific folder

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx download -s <sample-id> -d <absolute path of a directore/folder>


**In doubt, use --help everytime.**

.. code-block:: console

   singularity exec pxcli_0.1.0.sif projectx -h/--help

