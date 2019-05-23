##Gold rule for Cassandra##
#Satisfy a query by reading a single partition. This means we will use roughly one table per query. Supporting multiple query patterns usually means we need more than one table. Data duplication is encouraged.

#####################
CREATE  KEYSPACE KEYCHAIN WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 } ;
CREATE TABLE KEYCHAIN.KEYCHAIN ( address text PRIMARY KEY, type int, timestamp text, enc_keychain text, enc_addr text, prev_pubk text, prev_sig text, origin_sig text, validation_stamp text, cross_validation map<int,text>);
CREATE TABLE KEYCHAIN.ID ( address text PRIMARY KEY, type int, timestamp text, enc_aes_key text, enc_addr_miner text, enc_addr_self text, prev_pubk text, prev_sig text, origin_sig text, validation_stamp text, cross_validation map<int,text>);

#####################
CREATE  KEYSPACE SMARTCONTRACT WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 } ;
CREATE TABLE SMARTCONTRACT.SMARTCONTRACT (address text PRIMARY KEY, type int, timestamp text, ledger_UCO text, ledger_NFT text, ledger_stock_mgmt text, smartcontract text, content text, keys text, prev_pubk text, prev_sig text, origin_sig text, validation_stamp text, cross_validation map<int,text>);

#####################
CREATE  KEYSPACE LEDGER WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
CREATE TABLE LEDGER.UCO_LEDGER ();

