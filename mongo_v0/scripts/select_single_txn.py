import sys
import time
import hashlib
from pymongo import MongoClient
                       
def main():

    #Connect to the DB
    client = MongoClient(port=27017)
    db = client["smartcontract"]
    col = db["smartcontract"]

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    
    #Start a timer
    start_time = time.time()

	#execute the query on the DB
    txn = col.find_one({"address": ADDR})
	
    elapsed_time = time.time() - start_time
    print "Selecting one Txn takes: " , elapsed_time , "seconds"

    print txn


if __name__ == "__main__":
	main()