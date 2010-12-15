Intro
=====
couchdb-funsize takes a couchdb database and samples it to make a smaller database.
This is useful if you're trying to test views and you're spending more time
browsing YouTube while your views rebuild instead of working.

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
