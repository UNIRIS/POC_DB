import sys
import os
import time
import hashlib
from pymongo import MongoClient
                       
def main():

    #Clean results file
    resultFilePath = 'TXNChain.txt';
 
    if os.path.exists(resultFilePath):
        os.remove(resultFilePath)

    #Connect to the DB
    client = MongoClient(port=27017)
    db = client["smartcontract"]
    col = db["smartcontract"]

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #open file for results
    f=open(resultFilePath, "a+")

    #Start a timer
    start_time = time.time()
    
    while PREVIOUS_PUBK != 'nil':
        #To be continued

    f.close()
    elapsed_time = time.time() - start_time
    print "Selecting one Txn takes: " , elapsed_time , "seconds"


if __name__ == "__main__":
	main()