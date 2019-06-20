## INTRODUCTION

This study was made to have the necessary metrics and hypothesis to choose the right NOSQL engine for Uniris Nodes

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
| Insert of a Txn chain composed from 10 Txn        |  0.0456340312958      | 0.0525307655334     | 0.00594997406006      |  0.00483798980713    |
|                                                   |  74M of Disk space    | 373M  of Disk space | 82M of Disk space     |  74M of Disk space   |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 100 Txn       |  0.267061948776       | 0.129609107971      |  0.0571138858795      |  0.0477669239044     |
|                                                   |  74M of Disk space    | 373M  of Disk space | 82M of Disk space     |  74M of Disk space   |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 1000 Txn      |  1.84541893005        | 0.897126913071      |  0.551510095596       |  0.468037128448      |
|                                                   |  77M of Disk space    | 374M of disk space  |  85M of Disk space    |  80M of disk space   |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 10000 Txn     |  14.4179930687        | 8.50966596603       |  5.24847602844        |  4.81066298485       |
|                                                   |  105M of Disk space   | 388M of disk space  |  112M of Disk space   |  99M of disk space   |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 100000 Txn    |  134.478055           | 84.6112642288       |  53.1811311245        |  53.7913658619       |
|                                                   |  384M of Disk Space   | 521M of Disk Space  |  388M of Disk space   |  319M of Disk space  |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 1000000 Txn   |  1347.6940248         | 845.405930996       |  524.797007084        |  602.031270981       |
|                                                   |  1.3G of Disk space   | 1.9G of Disk space  |  3.1G of Disk space   |  2.5G of Disk space  |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 10000000 Txn  |  13434.3231409        | 8409.21618295       |  5263.31707096        |   7980.68224788      |
|                                                   |  13G                  | 15G of Disk space   |  31G of Disk space    |   23G of Disk space  |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |
| Insert of a Txn chain composed from 100000000 Txn |                       |                     |  55798.2558019        |                      |
|                                                   |                       |                     |  300G of Disk space   |                      |
| ------------------------------------------------- | --------------------- | ------------------- | --------------------- | -------------------- |

## SELECT one TXN from a DB (maxtime of 5 random tests)

Bellow the results of the tests

| Action                                                       | Cassandra Observation | MongoDB Observation | Aerospike Observation |  LevelDB Observation  |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 10 Txn                  |  0.00366401672363     |  0.00255703926086   | 0.000259876251221     | 0.000114917755127     |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 100 Txn                 |  0.00314903259277     |  0.00249600410461   | 0.000192880630493     | 0.000167846679688     |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 1000 Txn                |  0.00375294685364     |  0.00318908691406   | 0.000200033187866     | 0.000460863113403     | 
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 10000 Txn               |  0.00283908843994     |  0.00892400741577   | 0.000194072723389     | 0.00281405448914      |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 100000 Txn              |  0.00325798988342     |  0.0675449371338    | 0.000202894210815     | 0.00731682777405      |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 1000000 Txn             |  0.00370097160339     |  0.384087085724     | 0.00022292137146      | 0.010302066803        |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 10000000 Txn            |  0.00622200965881     |  100.191411018 *    | 0.000756025314331     | 0.0431909561157       |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn from a DB containing 100000000 Txn           |                       |                     | 0.000735998153687     |                       |
| ------------------------------------------------------------ | --------------------- | ------------------- | --------------------- | --------------------- |

* mongodb takes a long time when an entry is not yet on the memory, after each search the entry is keeped on the memory so after a first request (100s) the seconds one for the same entry take about (2s).

## SELECT A TXN chain from a DB containing 100000000 Txn (more than 150G of DATA)   (maxtime of 5 random tests)

Bellow the results of the tests

| Action                                           | Cassandra Observation | MongoDB Observation | Aerospike Observation |  LevelDB Observation  |
| -------------------------------------------------| --------------------- | ------------------- | --------------------- | --------------------- |
| Select one  Txn chain of 10                      |                       |                     | 0.00119090080261      |                       |
| Select one  Txn chain of 100 Txn                 |                       |                     | 0.0448069572449       |                       |
| Select one  Txn chain of 1000 Txn                |                       |                     | 0.422235965729        |                       |
| Select one  Txn chain of 10000 Txn               |                       |                     | 4.07087206841         |                       |
| Select one  Txn chain of 100000 Txn              |                       |                     | 41.7022249699         |                       |
| Select one  Txn chain of 1000000 Txn             |                       |                     | 435.582072973         |                       |
| -------------------------------------------------| --------------------- | ------------------- | --------------------- | --------------------- |


## RAM usage when stressing the DB instance whith many work (more than 150G of DATA in the DB)

Action performed to stress the DB:

* Random txn chain select.
* Random txn select
* Random writing

| Cassandra Observation | MongoDB Observation | Aerospike Observation |  LevelDB Observation  |
| --------------------- | ------------------- | --------------------- | --------------------- |
|                       |                     |                       |                       |
|                       |                     |                       |                       |
| --------------------- | ------------------- | --------------------- | --------------------- |



## GET BALANCE (UCO) of one Address from a memory View containing 10 million lines

Bellow the results of the tests

| Action                                           | Redis Observation     | AeroSpike Observation | 
| -------------------------------------------------| --------------------- | --------------------- | 
| Get Balance                                      |                       |                       |

