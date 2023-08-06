Tests ERP5 Appliance https://svn.erp5.org/repos/public/erp5/trunk/buildout/

There are two binaries available:

 - erp5apptest212
 - erp5apptest28

First one is used to test README for Zope 2.12 flavour, second to test Zope 2.8
flavour of ERP5 Appliance buildout.

Running any of those binaries with -h option will give command line help.

Example run
-----------

Create directory for testing:

 $ mkdir -p ~/apptest/run

Run erp5apptest212 once, with log:

 $ erp5apptest212 -v -s -o -l ~/apptest/run.log ~/apptest/run

After being run in ~/apptest/run.log full log of ERP5 Appliance run will be
available.
