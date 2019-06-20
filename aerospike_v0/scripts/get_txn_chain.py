import sys
import os
import time
import hashlib
import aerospike


def main():

    #Vars
    txnChain = []

    #Connect to the DB
    config = { 'hosts': [ ( '127.0.0.1', 3000 ) ], 'policies': { 'timeout': 1000  }}
    client = aerospike.client(config)
    client.connect()

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #Start a timer
    start_time = time.time()

    while PREVIOUS_PUBK != 'nil':
        key = ('on-disk-db', 'smartcontracts', ADDR)
        (key, metadata, record) = client.get(key)
        PREVIOUS_PUBK = record['prev_pubk']
        ADDR = hashlib.sha256(PREVIOUS_PUBK).hexdigest()
        txnChain.append(record)

    elapsed_time = time.time() - start_time
    print "Selecting TxnChain takes: " , elapsed_time , "seconds"
    #print txnChain


if __name__ == "__main__":
        main()
