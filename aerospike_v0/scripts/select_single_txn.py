import sys
import time
import hashlib
import aerospike

def main():

    #Connect to the DB
    config = { 'hosts': [ ( '127.0.0.1', 3000 ) ], 'policies': { 'timeout': 1000  }}
    client = aerospike.client(config)
    client.connect()

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()

    #GEN query
    key = ('on-disk-db', 'smartcontracts', ADDR)

    #Start a timer
    start_time = time.time()

    #execute the query on the DB
    (key, metadata, record) = client.get(key)

    elapsed_time = time.time() - start_time

    print "Selecting one Txn takes: " , elapsed_time , "seconds"

    print key
    print metadata
    print record


if __name__ == "__main__":
    main()
