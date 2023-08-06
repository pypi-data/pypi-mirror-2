# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = matter
PACKAGE = 

#--------------------------------------------------------------------------
#

BUILD_DIRS = \
	Parsers \
	atomic_properties \
	crystalIO \
	crystalUtils \
	
OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	Atom.py \
	AtomLoader2.py \
	AtomicObject.py \
	Lattice.py \
	PDFFitStructure.py \
	Site.py \
	SpaceGroups.py \
	Structure.py \
	StructureErrors.py \
	StructureManipulator.py \
	SymmetryUtilities.py \
	UnitCell.py \
	__init__.py \
	properties.py \
	sgtbxspacegroups.py \
	utils.py \
	version.py \
	wyckoff.py \
	__init__.py \


export:: export-package-python-modules

# version
# $Id$

# End of file
