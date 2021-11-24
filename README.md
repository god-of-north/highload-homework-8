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
siege -c10 -t10s -q http://localhost:5000/add/1

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    758 hits          764 hits          767 hits
Availability:                 100.00 %          100.00 %          100.00 %
Elapsed time:                  59.49 secs        59.08 secs        59.08 secs
Data transferred:               0.00 MB           0.00 MB           0.00 MB
Response time:                  0.27 secs         0.26 secs         0.24 secs
Transaction rate:              12.74 trans/sec   12.93 trans/sec   12.98 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                    3.45              3.34              3.12
Successful transactions:         758               764               767
Failed transactions:               0                 0                 0
Longest transaction:            1.94              1.13              1.95
Shortest transaction:           0.04              0.08              0.04
```


Testing innodb_flush_log_at_trx_commit parameter (concurrency=50):

```
siege -c50 -t10s -q http://localhost:5000/add/1

innodb_flush_log_at_trx_commit     0                 1                 2
Transactions:                    943 hits          832 hits         1048 hits
Availability:                 100.00 %          100.00 %          100.00 %
Elapsed time:                  59.85 secs        59.54 secs        59.17 secs
Data transferred:               0.00 MB           0.00 MB           0.00 MB
Response time:                  2.44 secs         2.81 secs         2.24 secs
Transaction rate:              15.76 trans/sec   13.97 trans/sec   17.71 trans/sec
Throughput:                     0.00 MB/sec       0.00 MB/sec       0.00 MB/sec
Concurrency:                   38.38             39.33             39.72
Successful transactions:         943               832              1048
Failed transactions:               0                 0                 0
Longest transaction:            7.83              5.97              7.32
Shortest transaction:           0.07              0.88              0.06
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

