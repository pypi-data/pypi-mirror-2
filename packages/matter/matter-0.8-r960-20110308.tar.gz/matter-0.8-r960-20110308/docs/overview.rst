Overview
========

Two types of data objects
-------------------------
The atom, lattice, and structure classes are built with several principles in mind:

* Most users will want "out-of-the-box" functionality in as many ways as possible.  They would like the ability to access diffraction thermal factors, forces, pseudopotentials, neutron-scattering cross sections, and so on.

* A smaller group of users will want slim data objects with a bare minimum of methods and information.  Although the speed gains will be small, the speed-up from using simpler dataobjects is critical.  Another rationale for wanting as-slim-as-possible dataobjects is because they do not want to continue to develop these data objects for their own purposes and do not want to take the time to learn about all the available methods and attributes.  

Fortunately, both of these aims can be met through adjusting which properties are included in primarily the Atom class using AtomPropertyCurator metaclass.  Users wanting the second type of dataobjects should adjust this metaclass in the desired manner. 

Spacegroup information
----------------------
Spacegroups are classes put together from lists of operations.  The list is gathered from Pymmlib and the sgtbx toolbox of cctbx.  Structure class persists a spacegroup identifier which is used to find spacegroup information for an individual symmetry group.

Matter data objects can be persisted
------------------------------------
Structure, lattice, and Atom data objects can seamlessly be persisted to most open source dbs using the dsaw object relational mapper.
