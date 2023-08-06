Smart Pool 
=====================

smartpool is forked from the python 2.7.1, but should work with 2.6.x.

smartpool adds two function to the default pool class right now:

* get_tracebacks(), returns a list of string-formatted tracebacks for each process in the pool
* resize(processes), increses or decreases the size of the pool