import time
import hashlib
import string
from random import *
import plyvel
                       
def main():
    
    #STATIC VARS
    dbDir = "/DATA/leveldb/onDiskDB"
    TYPE = 1
    PREVIOUS_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    ORIGIN_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    VALIDATION_STAMP = "NjUgNDAgMjMgNzEgNDEgMTIgYWQgMDggMjcgMzAgMmEgZWUgYzUgNWUgMjMgOGMgCjEyIGEzIDY5IDE5IDk4IDRhIGYzIGNiIGEzIGFhIDE4IDJjIGU3IDhlIDRiIDFhIAo1YiA0ZCBhZCBjYyA4NCBkOSBkOCBhMSBiYSBkNSA3ZCA3OSBlNCBlYSA0MSA2ZiAKMjggOGUgZmQgN2UgZTMgMmEgYjYgNzAgNDMgZjEgMzUgNzkgZGMgZDYgNDAgYmQgCjFhIGM4IDg4IGEyIGQ1IGEzIDQyIGVjIGY2IGM0IGE1IDM4IDk3IGUxIDc2IDkxIAoxZiAyZiA3MiBiNiA2YyBhZiAyMyAzZSA1YSA4MyAwZCAyNCA3MyAzYSBjNiA0OSAKMzMgZDEgYWYgNmMgYTggNTQgOGIgZTYgYjkgMjAgODUgMTEgOTggZTUgN2QgNjIgCmFjIDFiIDJlIGQ5IDdlIGExIDhkIGUzIDFkIGMxIDQwIDYzIDQ3IDQyIDVjIGNlIApiYyAzNSBlNSAyYSBiZSA5YSBlMSBkNCBjNCA2MCBmYiA1NyA5NyA2OSA5MiBhMyAKZjggNDIgZTIgNTYgOGYgMzYgNWUgMGYgM2QgOTkgNzQgYmYgYTUgZmMgZjYgNzggCmRmIDVhIDE0IGI3IDNmIGE4IGE2IGE2IGQ0IGFlIDIyIDU0IGJjIGFjIGRhIDY1IApiNCA0NCBlNSA2NSBjMCA4MiBjMCAwYiA5ZSAxOCA4YSAzYSBmYSA2NiA3ZCBmYSAKOTYgYjcgNjMgZDUgYzUgZGIgMDQgM2Ug"
    CROSS_VALIDATION = { "1" : "MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg", "2" : "MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg"}
    min_char = 1000
    max_char = 1000
    allchar = string.ascii_letters + string.punctuation + string.digits
    i = 0
    nbTxn = 10000
    
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

    #Start a timer
    start_time = time.time()

    while i < nbTxn:

		#GENERATE TXN PUBLIC KEY
        if i == 0:
            PREVIOUS_PUBK = 'nil'
        else:
            PREVIOUS_PUBK = str(i-1)

		#GENERATE TXN ADDR
        ADDR = hashlib.sha256(str(i)).hexdigest()

		#GENERATE TXN RANDOM DATA
        DATA = "".join(choice(allchar) for x in range(randint(min_char, max_char)))

		#GENERATE TIMESTAMP
        TIMESTAMP = time.time()
	
        #INSERT DATA

        db_type.put(ADDR, str(TYPE)) 
        db_timestamp.put(ADDR, str(TIMESTAMP)) 
        db_ledger_UCO.put(ADDR, b'') 
        db_ledger_NFT.put(ADDR, b'') 
        db_ledger_stock_mgmt.put(ADDR, b'') 
        db_smartcontract.put(ADDR, DATA) 
        db_content.put(ADDR, b'') 
        db_keys.put(ADDR, b'') 
        db_prev_pubk.put(ADDR, PREVIOUS_PUBK) 
        db_prev_sig.put(ADDR, PREVIOUS_SIG) 
        db_origin_sig.put(ADDR, ORIGIN_SIG) 
        db_validation_stamp.put(ADDR, VALIDATION_STAMP) 
        db_cross_validation.put(ADDR, str(CROSS_VALIDATION))
        
        print "txn " + str(i) + " stored \n"
        
		#PROGRESS
        i+=1
	
    elapsed_time = time.time() - start_time
    print "Inserting ",nbTxn," Txns takes: ",elapsed_time,"seconds"
    db.close()


if __name__ == "__main__":
	main()
