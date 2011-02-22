Intro
=====
couchdb-funsize is a simple python script that takes a couchdb database and samples
it to make a smaller database. This is useful if you're trying to test views
and you're spending more time browsing YouTube while your views rebuild instead
of working. It is designed to be run from the command line. If this script is
near a .couchapprc file, it will use it.

Usage
=====
    Usage: funsize.py [options]

    Options:
      -h, --help            show this help message and exit
      -s TARGET_SIZE, --target-size=TARGET_SIZE
                            The target size of the database. Defaults to 10000
      -c CHUNK_SIZE, --chunk-size=CHUNK_SIZE
                            The number of docs to read at a time from the source
                            database. Defaults to 10.
      --server=SERVER       URI of the couchDB server (e.g. http://localhost:5984)
      --source=DBNAME       The source database
      --target=DBNAME       The destination database, defaults to the source
                            database + "-funsized"

Installation
============

`pip install -r requirements.txt`

Notes
=====
This script isn't that fast either. The transaction costs are pretty high
because we can't do bulk insertions.

TODO
====
eliminate need for CouchDB requirement (use httplib/urllib/urllib2)

