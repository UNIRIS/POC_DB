import time
import hashlib
import string
from random import *
from cassandra.cluster import Cluster

def main():

    #STATIC VARS
    TYPE = 1
    PREVIOUS_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    ORIGIN_SIG = "1HZwkjkeaoZfTSaJxDw6aKkxp45agDiEzNHGIYzk1Kl0WC8yXtTxkkqCtTt96oba3MNK3gHiL0Nzy0ju47+olMXSCHmOswZmq1IWH/IhdjV6rfTdTk1VWv2fU="
    VALIDATION_STAMP = "NjUgNDAgMjMgNzEgNDEgMTIgYWQgMDggMjcgMzAgMmEgZWUgYzUgNWUgMjMgOGMgCjEyIGEzIDY5IDE5IDk4IDRhIGYzIGNiIGEzIGFhIDE4IDJjIGU3IDhlIDRiIDFhIAo1YiA0ZCBhZCBjYyA4NCBkOSBkOCBhMSBiYSBkNSA3ZCA3OSBlNCBlYSA0MSA2ZiAKMjggOGUgZmQgN2UgZTMgMmEgYjYgNzAgNDMgZjEgMzUgNzkgZGMgZDYgNDAgYmQgCjFhIGM4IDg4IGEyIGQ1IGEzIDQyIGVjIGY2IGM0IGE1IDM4IDk3IGUxIDc2IDkxIAoxZiAyZiA3MiBiNiA2YyBhZiAyMyAzZSA1YSA4MyAwZCAyNCA3MyAzYSBjNiA0OSAKMzMgZDEgYWYgNmMgYTggNTQgOGIgZTYgYjkgMjAgODUgMTEgOTggZTUgN2QgNjIgCmFjIDFiIDJlIGQ5IDdlIGExIDhkIGUzIDFkIGMxIDQwIDYzIDQ3IDQyIDVjIGNlIApiYyAzNSBlNSAyYSBiZSA5YSBlMSBkNCBjNCA2MCBmYiA1NyA5NyA2OSA5MiBhMyAKZjggNDIgZTIgNTYgOGYgMzYgNWUgMGYgM2QgOTkgNzQgYmYgYTUgZmMgZjYgNzggCmRmIDVhIDE0IGI3IDNmIGE4IGE2IGE2IGQ0IGFlIDIyIDU0IGJjIGFjIGRhIDY1IApiNCA0NCBlNSA2NSBjMCA4MiBjMCAwYiA5ZSAxOCA4YSAzYSBmYSA2NiA3ZCBmYSAKOTYgYjcgNjMgZDUgYzUgZGIgMDQgM2Ug"
    CROSS_VALIDATION = {1 : 'MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg', 2 : 'MzUgYzcgZmQgMTYgMjQgNGMgYjUgNzkgNzUgMjcgZDUgZDggYTggMGIgYTcgOGUgCmY1IGExIGFmIGNkIGYwIDg4IGRkIGQzIDkxIDAzIDk2IGQwIGIyIDJjIDgxIGFjIAo1NyA4ZCBlNyBmYSAzMiBhYiAxNyA1OCA0ZSA2NyA2MiBkNiAyMyAzNyAyNSA1MCAKZTQgOTIgYTcgNzQgMmIgYzEgZjUgNmEgYTAgZGYgZmQgMzYgNGEgOTAgNWQgMmUgCjk5IGRhIDUzIDkzIGE1IDg0IDM5IDY5IGYwIDdhIDBjIDQwIGM3IDdhIDBlIGRmIAo0OSBhMiAzMSBmZiBkNyA5YyBhNyA3MSBkZSAzZCBkYyBkMCA4MCA1YSAxZSA0MSAKZTEgNGUgYmYgYjMgMmMgOTcgYmYgY2MgMWMgMTAgNTIg'}
    min_char = 1000
    max_char = 1000
    allchar = string.ascii_letters + string.punctuation + string.digits
    i = 0
    nbTxn = 100000

#Connect to the DB
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('smartcontract')

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

        #Write the TXN on the DB
        session.execute(
        """
        INSERT INTO SMARTCONTRACT (address, type, timestamp, ledger_UCO, ledger_NFT, ledger_stock_mgmt, smartcontract, content, keys, prev_pubk, prev_sig, origin_sig, validation_stamp, cross_validation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (ADDR, TYPE, str(TIMESTAMP), "", "", "", DATA, "", "", PREVIOUS_PUBK, PREVIOUS_SIG, ORIGIN_SIG, VALIDATION_STAMP , CROSS_VALIDATION))
        print "txn " + str(i) + " stored \n"
        #PROGRESS
        i+=1

    elapsed_time = time.time() - start_time
    print "Inserting ",nbTxn," Txns takes: ",elapsed_time,"seconds"


if __name__ == "__main__":
    main()
