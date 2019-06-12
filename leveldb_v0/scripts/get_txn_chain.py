import sys
import time
import hashlib
import plyvel
                       
def main():

    #STATIC VARS
    dbDir = "/DATA/leveldb/onDiskDB"
    txn = [None]*14
    txnChain = []

    #DEFINE DB
    db = plyvel.DB(dbDir, create_if_missing=True)
    db_type = db.prefixed_db(b'type-')
    db_timestamp = db.prefixed_db(b'timestamp-')
    db_ledger_UCO = db.prefixed_db(b'ledger_UCO-')
    db_ledger_NFT = db.prefixed_db(b'ledger_NFT-')
    db_ledger_stock_mgmt = db.prefixed_db(b'ledger_stock_mgmt-')
    db_smartcontract = db.prefixed_db(b'smartcontract-')
    db_content = db.prefixed_db(b'content-')
    db_keys = db.prefixed_db(b'keys-')
    db_prev_pubk = db.prefixed_db(b'prev_pubk-')
    db_prev_sig = db.prefixed_db(b'prev_sig-')
    db_origin_sig = db.prefixed_db(b'origin_sig-')
    db_validation_stamp = db.prefixed_db(b'validation_stamp-')
    db_cross_validation = db.prefixed_db(b'cross_validation-')

    i = str(sys.argv[1])

    #GEN address
    ADDR = hashlib.sha256(i).hexdigest()
    PREVIOUS_PUBK = str(i)

    #Start a timer
    start_time = time.time()
    
    while PREVIOUS_PUBK != 'nil':
        #execute the query on the DB
        txn[0] = ADDR
        txn[1] = db_type.get(ADDR)
        txn[2] = db_timestamp.get(ADDR)
        txn[3] = db_ledger_UCO.get(ADDR)
        txn[4] = db_ledger_NFT.get(ADDR)
        txn[5] = db_ledger_stock_mgmt.get(ADDR)
        txn[6] = db_smartcontract.get(ADDR)
        txn[7] = db_content.get(ADDR)
        txn[8] = db_keys.get(ADDR)
        txn[9] = db_prev_pubk.get(ADDR)
        txn[10] = db_prev_sig.get(ADDR)
        txn[11] = db_origin_sig.get(ADDR)
        txn[12] = db_validation_stamp.get(ADDR)
        txn[13] = db_cross_validation.get(ADDR)
        #Update Data
        PREVIOUS_PUBK = txn[9]
        txnChain.append(txn)
        #progress on the chain
        ADDR = hashlib.sha256(txn[9]).hexdigest()


    elapsed_time = time.time() - start_time
    print "Selecting the txn-chain  takes: " , elapsed_time , "seconds"
    print txnChain


if __name__ == "__main__":
	main()
