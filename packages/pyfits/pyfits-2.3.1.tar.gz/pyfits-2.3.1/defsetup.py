from __future__ import division # confidence high

import distutils.extension
import sys
import logging

pkg = [ "pyfits", "pyfits.tests" ]
 

try:
    import numpy
    ext_modules = [distutils.extension.Extension("pyfits.pyfitsComp",
                     ["src/compress.c", "src/fits_hcompress.c",
                      "src/fits_hdecompress.c", "src/fitsio.c",
                      "src/pliocomp.c", "src/pyfitsCompWrapper.c",
                      "src/quantize.c", "src/ricecomp.c",
                      "src/zlib.c", "src/inffast.c",
                      "src/inftrees.c", "src/trees.c"],
                      include_dirs = ["src", numpy.get_include()])]

except ImportError:
    ext_modules = ''
    logging.warn("NUMPY was not found.  It may not be installed or it may")
    logging.warn("not be in your PYTHONPATH")
    logging.warn("optional extension module pyfits.pyfitsComp failed to build")

# Reimplement distutils build_ext class to allow us to continue
# setup even if the extension fails to build.
from distutils.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):

   def run(self):
      try:
         _build_ext.run(self)
      except:
         distutils.log.warn(str(sys.exc_info()[1]))
         warn = "optional extension modules failed to build"
         logging.warn(warn)

   def build_extensions(self):
      for ext in self.extensions:

          try:
              self.build_extension(ext)
          except:
              distutils.log.warn(str(sys.exc_info()[1]))
              warn = "optional extension module %s failed to build" % (ext.name)
              logging.warn(warn)


setupargs = {
    'version' :                 "2.3.1",
    'description' :             "General Use Python Tools",
    'author' :                  "J. C. Hsu, Paul Barrett, Christopher Hanley, James Taylor, Michael Droettboom",
    'maintainer_email' :        "help@stsci.edu",
    'license' :                 "http://www.stsci.edu/resources/software_hardware/pyraf/LICENSE",
    'platforms' :               ["Linux","Solaris","Mac OS X","Win"],
    'ext_modules' :             ext_modules,
    'cmdclass' :                {'build_ext': build_ext,},
    'package_dir' :             { 'pyfits' : 'lib', 'pyfits.tests' : 'lib/tests' },
    'data_files' :              [ ( 'pyfits/tests', [ 'lib/tests/*.fits' ] ) ],
}
