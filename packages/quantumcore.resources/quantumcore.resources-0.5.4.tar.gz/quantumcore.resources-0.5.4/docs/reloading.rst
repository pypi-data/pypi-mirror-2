Resource Reloading
******************

Resource auto-reloading works the following way:

1. When a ResourceManager is receiving a call which means to print out the links to the resource clusters, it will ask the clusters to check of the clusters have modified resources.
2. Each cluster will go through it's list of resources (in ``self.data``) and ask the resource if it has been modified.
3. The resource will check whether it has been modified and if so will reload it's data and return ``True``.
4. If a resource has been modified it will the cluster has to recreate itself by calling merge. It will have another hash then 
5. The ResourceManager will then print the links as without reloading maybe now with different hashes.

It's important to note that staleness is not checked on delivering resources as this might break links. It's important to have the correct hash at the end of the link being associated with the contents of it.



