# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = plotlib
#PACKAGE = 

#--------------------------------------------------------------------------
#

BUILD_DIRS = \
	
OTHER_DIRS = 

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    Line.py \
    mlab.py \
    NcPlottable.py \
    NcPlottableSet.py \
    TextPlottable.py \
    triangulate.py \
    types.py \
    VnfPlot.py \  

export:: export-package-python-modules

#EXPORT_PYTHON_MODULES = \
#    __init__.py \
#    Line.py \
#    NcPlottable.py \
#    NcPlottableSet.py \
#    TextPlottable.py \  
    
#CP_F = rsync 
#EXPORT_DATA_PATH = $(EXPORT_ROOT)/modules/$(PROJECT)

#export-data-files::
#	mkdir -p $(EXPORT_DATA_PATH); \
#	for x in $(EXPORT_DATAFILES); do { \
#	  $(CP_F) $$x $(EXPORT_DATA_PATH)/ ; \
#        } done


# version
# $Id$

# End of file
