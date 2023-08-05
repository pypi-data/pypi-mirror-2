=======================================
Clusters: How they are named and merged
=======================================


Naming of generated files
=========================

Links can be generated either from single files or from clusters of merged files. Those 
source files might come from various packages and locations and thus naming clashes are
unavoidable (e.g. two packages providing a resource named ``style.css``). 

:mod:`quantumcore.resources` thus needs to avoid such name clashes and tries to do that
in the following way:

 * Each resource be it merged or not will be put into it's own cluster (eventually just
   containing one resource) 
 * Each cluster can have an optional name provided in the resource definition 
 * When a link to a cluster is created it needs a filename. This filename is generated from 
   the name of the cluster or a predefined name if it's the default cluster.
 * If there are multiple clusters with the same name (because not all resources could
   be merged into one) then the filename will be appended with a numerical suffix,
   e.g. ``style1.css``
   
 
How merging works
=================

Resources will be merged into clusters under certain conditions. Here is how
it works:

 * Resources can define a certain profile. A profile is a string which classifies
   a resource. This can e.g. be based on the media type.
 * If a Resource is marked as non-mergeable, it will have a unique profile string so
   merging will never happen, because
 * only Resources with the same profile can be merged together into a cluster.
 * Before merging resources will be sorted by their ``prio`` attribute
 * Only resources which define the same profile string and are next to each other can
   be merged together. This is important because esp. with CSS the sequence of those
   resources is very important. This also means that if there are 10 resources with the
   same profile string in sequence but the one in the middle defines itself as non-mergeable,
   there will be three clusters instead of just two in the end.
 * If the Resource Manager is asked to render links for a specific ``name`` then all 
   those clusters with this name are rendered. This can be more than one cluster and 
   the naming is defined as explained above.
   