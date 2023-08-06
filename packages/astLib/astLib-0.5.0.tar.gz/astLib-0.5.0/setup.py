# -*- coding: utf-8 -*-

import os
import glob
from distutils.core import setup
from distutils.command.build_ext import build_ext
from distutils.extension import Extension
import distutils.ccompiler
import distutils.command.config
import distutils.sysconfig
from pkg_resources import require
#from setuptools import setup

#setup(install_requires = ["numpy", "scipy", "pyfits", "PIL", "setuptools", "distribute"])

topDir=os.getcwd()
sourceDir="PyWCSTools"+os.path.sep+"libwcs"+os.path.sep

#oFiles=glob.glob(sourceDir+"*.o")
#print oFiles
oFiles=['PyWCSTools/libwcs/ujcread.o', 'PyWCSTools/libwcs/skybotread.o', 'PyWCSTools/libwcs/wcslib.o', 'PyWCSTools/libwcs/fitsfile.o', 'PyWCSTools/libwcs/catutil.o', 'PyWCSTools/libwcs/platefit.o', 'PyWCSTools/libwcs/imio.o', 'PyWCSTools/libwcs/hput.o', 'PyWCSTools/libwcs/matchstar.o', 'PyWCSTools/libwcs/distort.o', 'PyWCSTools/libwcs/sdssread.o', 'PyWCSTools/libwcs/ucacread.o', 'PyWCSTools/libwcs/fortwcs.o', 'PyWCSTools/libwcs/imsetwcs.o', 'PyWCSTools/libwcs/iget.o', 'PyWCSTools/libwcs/fileutil.o', 'PyWCSTools/libwcs/tnxpos.o', 'PyWCSTools/libwcs/ty2read.o', 'PyWCSTools/libwcs/wcsinit.o', 'PyWCSTools/libwcs/proj.o', 'PyWCSTools/libwcs/gsc2read.o', 'PyWCSTools/libwcs/tmcread.o', 'PyWCSTools/libwcs/webread.o', 'PyWCSTools/libwcs/imhfile.o', 'PyWCSTools/libwcs/ctgread.o', 'PyWCSTools/libwcs/imutil.o', 'PyWCSTools/libwcs/platepos.o', 'PyWCSTools/libwcs/ubcread.o', 'PyWCSTools/libwcs/daoread.o', 'PyWCSTools/libwcs/gscread.o', 'PyWCSTools/libwcs/findstar.o', 'PyWCSTools/libwcs/lin.o', 'PyWCSTools/libwcs/tabread.o', 'PyWCSTools/libwcs/hget.o', 'PyWCSTools/libwcs/wcscon.o', 'PyWCSTools/libwcs/cel.o', 'PyWCSTools/libwcs/imrotate.o', 'PyWCSTools/libwcs/binread.o', 'PyWCSTools/libwcs/dateutil.o', 'PyWCSTools/libwcs/dsspos.o', 'PyWCSTools/libwcs/sph.o', 'PyWCSTools/libwcs/imgetwcs.o', 'PyWCSTools/libwcs/sortstar.o', 'PyWCSTools/libwcs/wcs.o', 'PyWCSTools/libwcs/actread.o', 'PyWCSTools/libwcs/fitswcs.o', 'PyWCSTools/libwcs/worldpos.o', 'PyWCSTools/libwcs/wcstrig.o', 'PyWCSTools/libwcs/uacread.o']

exampleScripts=glob.glob("scripts"+os.path.sep+"*.py")

class build_PyWCSTools_ext(build_ext):
	
    def build_extensions(self):
        
        os.chdir(sourceDir)
        
        cc=distutils.ccompiler.new_compiler(distutils.ccompiler.get_default_compiler())
        distutils.command.config.customize_compiler(cc)
        
        # Suppress warnings from compiling WCSTools libwcs
        if "-Wstrict-prototypes" in cc.compiler_so:
            cc.compiler_so.pop(cc.compiler_so.index("-Wstrict-prototypes"))
        if "-Wall" in cc.compiler_so:
            cc.compiler_so.pop(cc.compiler_so.index("-Wall"))

        WCSToolsCFiles=glob.glob("*.c")
        WCSToolsCFiles.pop(WCSToolsCFiles.index("wcs_wrap.c"))
        WCSToolsCFiles.pop(WCSToolsCFiles.index("wcscon_wrap.c"))
        cc.compile(WCSToolsCFiles)
        
        os.chdir(topDir)
        
        build_ext.build_extensions(self)		

setup(name='astLib',
    version='0.5.0',
    url='http://astlib.sourceforge.net',
    author='Matt Hilton',
    author_email='mattyowl@users.sourceforge.net',
    classifiers=['Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
            'Natural Language :: English',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Astronomy',
            'Topic :: Software Development :: Libraries'],
    description='A set of python modules for producing simple plots, statistics, common calculations, coordinate conversions, and manipulating FITS images with World Coordinate System (WCS) information.',
    long_description="""astLib is a set of Python modules that provides some tools for research astronomers. It can be
    used for simple plots, statistics, common calculations, coordinate conversions, and manipulating FITS images
    with World Coordinate System (WCS) information through PyWCSTools - a simple wrapping of WCSTools by Doug Mink.
    PyWCSTools is distributed (and developed) as part of astLib.""",
    packages=['astLib', 'PyWCSTools'],
    package_data={'astLib': ['data/*']},
    cmdclass={"build_ext": build_PyWCSTools_ext},
    scripts=exampleScripts,
    ext_modules=[
        Extension('PyWCSTools._wcscon', [sourceDir+"wcscon_wrap.c"], 
        extra_objects=oFiles),
        Extension('PyWCSTools._wcs', [sourceDir+"wcs_wrap.c"], 
        extra_objects=oFiles)
    ]
	)
