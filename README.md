# Homework #4 for Highload:Projector

Database optimization

## Installation

```
git clone https://github.com/god-of-north/highload-homework-8.git
cd highload-homework-4 
docker-compose build
docker-compose run
curl -X GET http://localhost:5000/add/40000000
```

## Testing insertion speed


Testing innodb_flush_log_at_trx_commit parameter (concurrency=10):

```
siege -c10 -t10s -q http://localhost:5000/test

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    614 hits          202 hits          475 hits
Availability:                 100.00 %           20.95 %           54.98 %
Elapsed time:                  59.82 secs        63.48 secs        59.73 secs
Data transferred:               0.00 MB           0.21 MB           0.11 MB
Response time:                  0.49 secs         0.71 secs         0.34 secs
Transaction rate:              10.26 trans/sec    3.18 trans/sec    7.95 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                    4.99              2.27              2.74
Successful transactions:         614               202               475
Failed transactions:               0               762               389
Longest transaction:            1.90              1.45              1.63
Shortest transaction:           0.04              0.00              0.00
```


Testing innodb_flush_log_at_trx_commit parameter (concurrency=50):

```
siege -c50 -t10s -q http://localhost:5000/test

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    713 hits          508 hits          631 hits
Availability:                 100.00 %          100.00 %          100.00 %
Elapsed time:                  59.11 secs        60.01 secs        59.71 secs
Data transferred:               0.00 MB           0.00 MB           0.00 MB
Response time:                  3.52 secs         5.12 secs         4.04 secs
Transaction rate:              12.06 trans/sec    8.47 trans/sec   10.57 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                   42.42             43.33             42.74
Successful transactions:         713               508               631
Failed transactions:               0                 0                 0
Longest transaction:            5.28              7.88              6.88
Shortest transaction:           0.52              0.64              0.15
```


## Testing indexies 


Testing queries:

```
SELECT count(*) 
from users use index(btree_index)
where birth_day  between '2000-01-01' and '2018-01-31';
-- Average time:    btree:11s		hash:12.7s		no index:1.5m

SELECT count(*) 
from users use index(btree_index)
where birth_day = '2005-10-10';
-- Average time:    btree:5ms 		hash:4ms		no index:1.1m

SELECT count(*) 
from users use index(btree_index)
where birth_day > '2005-10-10';
-- Average time:    btree:3.2s		hash:2.7s		no index:1.15m

SELECT count(*) 
FROM users use index(btree_index)
WHERE birth_day <= now() - INTERVAL 18 YEAR and
      birth_day > now() - INTERVAL 26 YEAR ;
-- Average time:    btree:6.4ms		hash:7.4s		no index:1.28m
      
SELECT count(*) 
from users use index(btree_index)
where MONTH(birth_day) = 1 and
      DAY(birth_day) = 1;
-- Average time:    btree:16.5s		hash:16.6s		no index:1.15m

SELECT count(*) 
FROM users use index(btree_index)
WHERE birth_day < now() - INTERVAL 18 YEAR;
-- Average time:    btree:17.4s		hash:17.8s		no index:1.17m
```

