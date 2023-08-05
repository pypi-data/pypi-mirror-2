#!/usr/bin/env python
""" 
caPyGen API Generation
"""

__author__ = 'Konrad Rokicki'
__date__ = '$Date$'
__version__ = '$Revision$'

import sys
import os
from ZSI.generate.commands import wsdl2py
from distutils import dir_util, file_util
import cacore2python
    
NS_INIT= ("__import__('pkg_resources').declare_namespace(__name__)",)

def cacore2py():

    # Find settings.py
    try:
        sys.path.insert(0,'.')
        import settings # Assumed to be in the current working directory.
    except ImportError:
        sys.stderr.write("Error: Can't find settings.py\n")
        sys.exit(1)
    
    print "Cleaning output directory",settings.OUTPUT_DIR
    
    # Clean output dir
    try:
        dir_util.remove_tree(settings.OUTPUT_DIR)
    except OSError:
        pass
    
    r = [settings.OUTPUT_DIR,]+settings.ROOT_PACKAGE.split('.')
    outputDir = os.path.join(*r)
    dir_util.mkpath(settings.OUTPUT_DIR)
    
    print "Generating Python API from",settings.WSDL_FILE
    
    # Recreate output tree with __init__.py files at each level
    for p in [settings.ROOT_PACKAGE+"."+v for v in settings.PACKAGE_MAPPING.values()]:
        prefix = settings.OUTPUT_DIR
        # p is something like "cabig.cabio.common.domain"
        # Now iterate thru each prefix of p, "cabig/", "cabig/cabio/", etc
        # But don't create a directory for the leaf, since it will be a module.
        for d in p.split('.')[:-1]: 
            prefix = os.path.join(prefix,d)
            dir_util.mkpath(prefix)
            # The "cabig" package is a namespace package.
            contents = ''
            if d == 'cabig': contents = NS_INIT
            # Yes, this might write the same file several times, not a big deal.
            file_util.write_file(os.path.join(prefix,'__init__.py'),contents)
    
    # Generate ZSI API (*services.py and *_services_types.py)
    # Note that we must use the "-l" option here to do lazy evaluation of type 
    # codes, necessary to support 1-to-1 associations in caCORE-like systems.
    args = ['-lbo', outputDir, settings.WSDL_FILE]
    wsdl2py(args)
    
    # A really ugly way of dynamically loading the module we just generated.
    # The __import__ function doesn't seem to like packages though...
    sys.path.insert(0,outputDir)
    fileName = [f for f in os.listdir(outputDir) if f.endswith('_client.py')][0]
    moduleName = fileName.replace('.py','')
    module = __import__(moduleName)
    
    # Generate a nicer caCORE-like API on top of the ZSI one
    cacore2python.generate(module, settings, outputDir)

    print "API generation completed"


if __name__ == "__main__":
    cacore2py()
    