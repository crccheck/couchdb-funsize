#!/usr/bin/python
#import logging
try:
    import simplejson as json
except ImportError:
    import json
import couchdb
import os
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--target-size", dest="target_size", default=10000,
                  help="The target size of the database. Defaults to 10000")
parser.add_option("-c", "--chunk-size", dest="chunk_size", default=10,
                  help="The number of docs to read at a time from the source database. Defaults to 10.")
parser.add_option("--server", dest="server",
                  help="URI of the couchDB server (e.g. http://localhost:5984)")
parser.add_option("--source", dest="src_dbname", metavar="DBNAME",
                  help="The source database")
parser.add_option("--target", dest="dst_dbname", metavar="DBNAME",
                  help='The destination database, defaults to the source database + "-funsized"')

settings, args = parser.parse_args()

# TODO exit properly in good times and bad

def find_rc():
    rcfile = '.couchapprc'
    if os.path.isfile(rcfile):
        return rcfile
    rcfile = '../.couchapprc'
    if os.path.isfile(rcfile):
        return rcfile
    return None

def couch_start():
    if not settings.server and not settings.src_dbname:
        rcfile = find_rc()
        if rcfile:
            data = json.load(open(rcfile), 'r')
            DATABASE = data['env']['default']['db'].rsplit('/', 1)
            settings.server = DATABASE[0]
            settings.src_dbname = DATABASE[1]
    if not settings.server and not settings.src_dbname:
        sys.exit("Can't find a server or source database or couchapprc")
    if not settings.dst_dbname:
        settings.dst_dbname = "%s-funsize" % settings.src_dbname
    server = couchdb.client.Server(settings.server)
    try:
        src_db = server[settings.src_dbname]
        if settings.dst_dbname in server:
            overwrite = raw_input("Target database exists. Overwrite (Y/n)?")
            if overwrite in ['', 'y', 'Y']:
                del server[settings.dst_dbname]
            else:
                raise Exception("I'm not allowed to delete databases")
        dst_db = server.create(settings.dst_dbname)
    except couchdb.ResourceNotFound as e:
        raise e
    print "Using server: %s. Source database: %s. Target database: %s." % (settings.server, settings.src_dbname, settings.dst_dbname)
    print "Target Size: %s. Chunk Size: %s" % (settings.target_size, settings.chunk_size)
    return src_db, dst_db

def main():
    def get_row_count():
        v = src_db.view('_all_docs', limit=0)
        return v.total_rows
    settings.target_size = int(settings.target_size)
    settings.chunk_size = int(settings.chunk_size)
    src_db, dst_db = couch_start()
    n = get_row_count()
    if n < settings.target_size:
        sys.exit('Source database already small enough')
    skip_size = settings.chunk_size * n / settings.target_size
    i = 1
    for skip in xrange(0, n-settings.chunk_size, skip_size):
        v = src_db.view('_all_docs', skip=skip, limit=settings.chunk_size)
        for row in v.rows:
            if row.key[0] != '_':
                doc = src_db[row.key]
                dst_db[row.key] = doc
                i += 1
                if i > settings.target_size:
                    break;
                if not i % 500:
                    print "Copied %d/%d" % (i, settings.target_size)
    print "Finished. Copied %d docs to %s/%s" % (i - 1, settings.server, settings.dst_dbname)


#logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "^C HALT"
        sys.exit(1)
