import sys
import os
import time
import hashlib
from pymongo import MongoClient

def main():

    #Vars
    txnChain = []

    #Connect to the DB
    client = MongoClient(port=27017)
    db = client["smartcontract"]
    col = db["smartcontract"]

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #Start a timer
    start_time = time.time()

    while PREVIOUS_PUBK != 'nil':
        txn = col.find_one({"address": ADDR})
        PREVIOUS_PUBK = txn['prev_pubk']
        ADDR = hashlib.sha256(PREVIOUS_PUBK).hexdigest()
        txnChain.append(txn)

    elapsed_time = time.time() - start_time
    print "Selecting TxnChain takes: " , elapsed_time , "seconds"
    print txnChain


if __name__ == "__main__":
        main()
