==============================
pyCaCORE
==============================

This library is both a Python API generator for caCORE-like systems, 
and a runtime library required for using the generated APIs. 


Prerequisites
-------------
Python 2.5 or greater

Latest setuptools
  To install, download and execute the following script:
  http://peak.telecommunity.com/dist/ez_setup.py

The installation uses setuptools to automatically install any 
other dependencies.


Installation
------------
System-wide install:

    python setup.py install

Single user install:

    python setup.py install --home=~


API Generation
--------------
After installing this library, you will have access to a script called
cacore2py, which is usually installed in /usr/bin. You can create an 
API for any caCORE-like system as follows:

1) Download the WSDL for the caCORE-like system.

   Currently you also need to modify the WSDL according to the instructions 
   provided in cabig/cacore/ws/axis.py
   In the future, this will be automated.

2) Create a settings.py for your system. Use example_settings.py as 
   a template. 

3) Run cacore2py to generate the API to ./output/


Known Issues
------------
* Sending arrays (collections) is not possible due to a conflict between AXIS 
  and ZSI.
  

Change History
--------------
0.1.0 - 07/01/2008
Initial alpha release

0.2.0 - 08/18/2008
Fixed GF16157 - Only one association may be retrieved




