# Homework #4 for Highload:Projector

Database optimization

## Installation

```
git clone https://github.com/god-of-north/highload-homework-8.git
cd highload-homework-4 
docker-compose build
docker-compose run
curl -X GET http://localhost:5000/add/40000
```

## Testing insertion speed


Testing innodb_flush_log_at_trx_commit parameter (concurrency=10):

```
siege -c10 -t10s -q http://localhost:5000/add/1

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    162 hits          136 hits          160 hits
Availability:                 100.00 %          100.00 %          100.00 %
Elapsed time:                   9.85 secs         9.98 secs         9.59 secs
Data transferred:               0.00 MB           0.00 MB           0.00 MB
Response time:                  0.13 secs         0.21 secs         0.10 secs
Transaction rate:             16.45 trans/sec    13.62 trans/sec   16.68 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                    2.16              2.84              1.74
Successful transactions:         162               136               160
Failed transactions:               0                 0                 0
Longest transaction:            0.46              0.52              0.24
Shortest transaction:           0.05              0.08              0.05
```


Testing innodb_flush_log_at_trx_commit parameter (concurrency=50):

```
siege -c100 -t10s -q http://localhost:5000/add/1

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    347 hits          189 hits          405 hits
Availability:                 100.00 %          100.00 %          100.00 %
Elapsed time:                  9.55 secs          9.48 secs         9.15 secs
Data transferred:               0.00 MB           0.00 MB           0.00 MB
Response time:                  0.76 secs         1.70 secs         0.60 secs
Transaction rate:              36.33 trans/sec   19.93 trans/sec   44.24 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                   27.71             33.88             26.53
Successful transactions:         347               189               405
Failed transactions:               0                 0                 0
Longest transaction:            1.39              2.17              1.10
Shortest transaction:           0.08              0.10              0.16
```


## Testing indexies 


Testing queries:

```
SELECT count(*) 
from users use index(btree_index)
where birth_day  between '2000-01-01' and '2018-01-31';
-- Average time:    btree:70ms    hash: 72ms    no_index: 147ms

SELECT count(*) 
from users use index(btree_index)
where birth_day = '2005-10-10';
-- Average time:    btree:5ms     hash: 6ms     no_index: 134ms

SELECT count(*) 
from users use index(btree_index)
where birth_day > '2005-10-10';
-- Average time:    btree:19ms    hash: 14ms    no_index: 71ms

SELECT count(*) 
FROM users use index(btree_index)
WHERE birth_day <= now() - INTERVAL 18 YEAR and
      birth_day > now() - INTERVAL 26 YEAR ;
-- Average time:    btree:47ms    hash: 40ms    no_index: 116ms
      
SELECT count(*) 
from users use index(btree_index)
where MONTH(birth_day) = 1 and
      DAY(birth_day) = 1;
-- Average time:    btree:62ms    hash: 66ms    no_index: 55ms

SELECT count(*) 
FROM users use index(btree_index)
WHERE birth_day < now() - INTERVAL 18 YEAR;
-- Average time:    btree:78ms    hash: 49ms    no_index: 83ms
```
