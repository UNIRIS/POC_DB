import sys
import time
import hashlib
from cassandra.cluster import Cluster
                       
def main():

    #Connect to the DB
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('smartcontract')
    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()

    #GEN query
    query = "SELECT * FROM SMARTCONTRACT where address = '" + ADDR + "'"
    
    #Start a timer
    start_time = time.time()

	#execute the query on the DB
    txn = session.execute(query)
	
    elapsed_time = time.time() - start_time

    for row in txn:
        print row

    print "Selecting one Txn takes: " , elapsed_time , "seconds"


if __name__ == "__main__":
	main()