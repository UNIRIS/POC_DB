import sys
import os
import time
import hashlib
from cassandra.cluster import Cluster

def main():

    #Vars
    txnChain = []
    txn = [None]*14

    #Connect to the DB
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('smartcontract')
    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #Start a timer
    start_time = time.time()

    while PREVIOUS_PUBK != 'nil':
        #GEN query
        query = "SELECT * FROM SMARTCONTRACT where address = '" + ADDR + "'"

            #execute the query on the DB
        res = session.execute(query)

        for row in res:
            PREVIOUS_PUBK = row.prev_pubk
            ADDR = hashlib.sha256(row.prev_pubk).hexdigest()
            txn[0] = row.address
            txn[1] = row.type
            txn[2] = row.timestamp
            txn[3] = row.ledger_uco
            txn[4] = row.ledger_nft
            txn[5] = row.ledger_stock_mgmt
            txn[6] = row.smartcontract
            txn[7] = row.content
            txn[8] = row.keys
            txn[9] = row.prev_pubk
            txn[10] = row.prev_sig
            txn[11] = row.origin_sig
            txn[12] = row.validation_stamp
            txn[13] = row.cross_validation

        txnChain.append(txn)

    elapsed_time = time.time() - start_time
    print "Selecting Txnchain takes: " , elapsed_time , "seconds"
    print txnChain


if __name__ == "__main__":
    main()

