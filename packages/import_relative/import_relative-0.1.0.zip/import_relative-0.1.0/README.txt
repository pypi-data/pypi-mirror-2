A reduced Python __import__() function where one must give a directory for
which to start searching from.

As per __import__() sans "from lists" which is used here, we always
return the top-level import name even when a compound import
(e.g. a.b.c) is given.  

Sorry, we don't do "from lists", global or local variables here.
