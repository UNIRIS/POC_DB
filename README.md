## INTRODUCTION

This study was made to have the necessary metrics and hypothesis to choose the right NOSQL engine for Uniris Miners

## ASSUMPTIONS

### The uniris Miner will run on a intel NUC7I3 DNKE

- Datasheet here: https://www.intel.com/content/dam/support/us/en/documents/mini-pcs/nuc-kits/NUC7i3DN_TechProdSpec.pdf
- CPU info here: https://ark.intel.com/content/www/us/en/ark/products/95442/intel-core-i3-7100u-processor-3m-cache-2-40-ghz.html

- CPU is 2 core / 4 thread.
- RAM is up to 32G maximum.
- NVMe SSD up to 2TB


### Using this metrics we will suppose that:

* OnDISK DB should use a maximum of 8GB of RAM.
* OnMemory DB should use a maximum of 8GB of RAM.
* The remaining 16G of RAM will be used by the OS and by the Software.

## INSERT A TXN-Chain

Bellow the results of the tests

| Action                                            | Cassandra Observation | MongoDB Observation | Aerospike Observation | LevelDB Observation  |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 10 Txn        |  0.0456340312958 s    | 0.0525307655334     | 0.00594997406006 s    |  0.00483798980713    |
|                                                   |  74M of Disk space    | 373M  of Disk space | 82M of Disk space     |  74M of Disk space   |
| Insert of a Txn chain composed from 100 Txn       |
| Insert of a Txn chain composed from 1000 Txn      |
| Insert of a Txn chain composed from 10000 Txn     |
| Insert of a Txn chain composed from 100000 Txn    |
| Insert of a Txn chain composed from 1000000 Txn   |
| Insert of a Txn chain composed from 10000000 Txn  |

## SELECT one TXN from a DB

Bellow the results of the tests

| Action                                                       | Cassandra Observation | MongoDB Observation | Aerospike Observation |  LevelDB Observation  |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 10 Txn                  |  0.00366401672363     |  0.00255703926086   | 0.000259876251221     | 0.000114917755127     |
| Select one  Txn from a DB containing 100 Txn                 |
| Select one  Txn from a DB containing 1000 Txn                |
| Select one  Txn from a DB containing 10000 Txn               |
| Select one  Txn from a DB containing 100000 Txn              |
| Select one  Txn from a DB containing 1000000 Txn             |
| Select one  Txn from a DB containing 10000000 Txn            |


## SELECT A TXN chain from a DB containing 450G of DATA

Bellow the results of the tests

| Action                                           | Cassandra Observation | MongoDB Observation | Aerospike Observation |  LevelDB Observation  |
| -------------------------------------------------| --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn chain of 10                      | 
| Select one  Txn chain of 100 Txn                 |
| Select one  Txn chain of 1000 Txn                |
| Select one  Txn chain of 10000 Txn               |
| Select one  Txn chain of 100000 Txn              |
| Select one  Txn chain of 1000000 Txn             |
| Select one  Txn chain of 10000000 Txn            |


## GET BALANCE (UCO) of one Address from a memory View containing 10 million lines

Bellow the results of the tests

| Action                                           | Redis Observation     | AeroSpike Observation | 
| -------------------------------------------------| --------------------- | --------------------- | 
| Get Balance                    | 

