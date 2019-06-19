import time
import hashlib
import string
from random import *
import aerospike
                       
def main():
    
    #STATIC VARS
    TYPE = 1
    PREVIOUS_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    ORIGIN_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    VALIDATION_STAMP = "NjUgNDAgMjMgNzEgNDEgMTIgYWQgMDggMjcgMzAgMmEgZWUgYzUgNWUgMjMgOGMgCjEyIGEzIDY5IDE5IDk4IDRhIGYzIGNiIGEzIGFhIDE4IDJjIGU3IDhlIDRiIDFhIAo1YiA0ZCBhZCBjYyA4NCBkOSBkOCBhMSBiYSBkNSA3ZCA3OSBlNCBlYSA0MSA2ZiAKMjggOGUgZmQgN2UgZTMgMmEgYjYgNzAgNDMgZjEgMzUgNzkgZGMgZDYgNDAgYmQgCjFhIGM4IDg4IGEyIGQ1IGEzIDQyIGVjIGY2IGM0IGE1IDM4IDk3IGUxIDc2IDkxIAoxZiAyZiA3MiBiNiA2YyBhZiAyMyAzZSA1YSA4MyAwZCAyNCA3MyAzYSBjNiA0OSAKMzMgZDEgYWYgNmMgYTggNTQgOGIgZTYgYjkgMjAgODUgMTEgOTggZTUgN2QgNjIgCmFjIDFiIDJlIGQ5IDdlIGExIDhkIGUzIDFkIGMxIDQwIDYzIDQ3IDQyIDVjIGNlIApiYyAzNSBlNSAyYSBiZSA5YSBlMSBkNCBjNCA2MCBmYiA1NyA5NyA2OSA5MiBhMyAKZjggNDIgZTIgNTYgOGYgMzYgNWUgMGYgM2QgOTkgNzQgYmYgYTUgZmMgZjYgNzggCmRmIDVhIDE0IGI3IDNmIGE4IGE2IGE2IGQ0IGFlIDIyIDU0IGJjIGFjIGRhIDY1IApiNCA0NCBlNSA2NSBjMCA4MiBjMCAwYiA5ZSAxOCA4YSAzYSBmYSA2NiA3ZCBmYSAKOTYgYjcgNjMgZDUgYzUgZGIgMDQgM2Ug"
    CROSS_VALIDATION = { "1" : "MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg", "2" : "MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg"}
    min_char = 1000
    max_char = 1000
    allchar = string.ascii_letters + string.punctuation + string.digits
    i = 0
    nbTxn = 1000

    #Connect to the DB
    config = { 'hosts': [ ( '127.0.0.1', 3000 ) ], 'policies': { 'timeout': 1000  }}
    client = aerospike.client(config)
    client.connect()

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
	
        key = key = ('on-disk-db', 'smartcontracts', ADDR)

        bins = {
            'type': TYPE, \
            'timestamp': TIMESTAMP, \
            'ledger_UCO': '', \
            'ledger_NFT': '', \
            'ledger_stock': '', \
            'smartcontract': DATA, \
            'content': '', \
            'keys': '', \
            "prev_pubk" : PREVIOUS_PUBK, \
            "prev_sig" : PREVIOUS_SIG, \
            "origin_sig" : ORIGIN_SIG, \
            "valid_stamp" : VALIDATION_STAMP, \
            "cross_valid" : CROSS_VALIDATION }

        client.put(key, bins)
        print "txn " + str(i) + " stored \n"

		#PROGRESS
        i+=1
	
    elapsed_time = time.time() - start_time
    print "Inserting ",nbTxn," Txns takes: ",elapsed_time,"seconds"


if __name__ == "__main__":
	main()
