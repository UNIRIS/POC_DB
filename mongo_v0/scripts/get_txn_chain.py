import sys
import os
import time
import hashlib
from cassandra.cluster import Cluster
                       
def main():

    #Clean results file
    resultFilePath = 'TXNChain.txt';
 
    if os.path.exists(resultFilePath):
        os.remove(resultFilePath)

    #Connect to the DB
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('smartcontract')
    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #open file for results
    f=open(resultFilePath, "a+")

    #Start a timer
    start_time = time.time()
    
    while PREVIOUS_PUBK != 'nil':
        #GEN query
        query = "SELECT * FROM SMARTCONTRACT where address = '" + ADDR + "'"
    
	    #execute the query on the DB
        txn = session.execute(query)
	    
        for row in txn:
            f.write(str(row)+'\n')
            PREVIOUS_PUBK = row.prev_pubk
            ADDR = hashlib.sha256(row.prev_pubk).hexdigest()

    f.close()
    elapsed_time = time.time() - start_time
    print "Selecting one Txn takes: " , elapsed_time , "seconds"


if __name__ == "__main__":
	main()