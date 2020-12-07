# без балансировки: 5000 запросов
ab -n 5000 -c 10 http://127.0.0.1/api/v2/questions
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 500 requests
Completed 1000 requests
Completed 1500 requests
Completed 2000 requests
Completed 2500 requests
Completed 3000 requests
Completed 3500 requests
Completed 4000 requests
Completed 4500 requests
Completed 5000 requests
Finished 5000 requests


Server Software:        nginx/1.19.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions
Document Length:        2604 bytes

Concurrency Level:      10
Time taken for tests:   508.860 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      14165000 bytes
HTML transferred:       13020000 bytes
Requests per second:    9.83 [#/sec] (mean)
Time per request:       1017.720 [ms] (mean)
Time per request:       101.772 [ms] (mean, across all concurrent requests)
Transfer rate:          27.18 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       3
Processing:   444 1017 171.4   1008    1905
Waiting:      444 1017 171.3   1007    1904
Total:        444 1017 171.4   1008    1905

Percentage of the requests served within a certain time (ms)
  50%   1008
  66%   1077
  75%   1123
  80%   1152
  90%   1234
  95%   1311
  98%   1423
  99%   1485
 100%   1905 (longest request)


# с балансировкой: 5000 запросов
ab -n 5000 -c 10 http://127.0.0.1/api/v2/questions
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 500 requests
Completed 1000 requests
Completed 1500 requests
Completed 2000 requests
Completed 2500 requests
Completed 3000 requests
Completed 3500 requests
Completed 4000 requests
Completed 4500 requests
Completed 5000 requests
Finished 5000 requests


Server Software:        nginx/1.19.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions
Document Length:        2604 bytes

Concurrency Level:      10
Time taken for tests:   512.274 seconds
Complete requests:      5000
Failed requests:        0
Total transferred:      14165000 bytes
HTML transferred:       13020000 bytes
Requests per second:    9.76 [#/sec] (mean)
Time per request:       1024.548 [ms] (mean)
Time per request:       102.455 [ms] (mean, across all concurrent requests)
Transfer rate:          27.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       6
Processing:   467 1024 168.1   1024    1703
Waiting:      467 1024 168.1   1024    1703
Total:        467 1024 168.1   1024    1703

Percentage of the requests served within a certain time (ms)
  50%   1024
  66%   1086
  75%   1126
  80%   1152
  90%   1238
  95%   1312
  98%   1393
  99%   1467
 100%   1703 (longest request)

# без балансировки: 10000 запросов
ab -n 10000 -c 10 http://127.0.0.1/api/v2/questions/1
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        nginx/1.19.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions/1
Document Length:        1582 bytes

Concurrency Level:      10
Time taken for tests:   317.799 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      18050000 bytes
HTML transferred:       15820000 bytes
Requests per second:    31.47 [#/sec] (mean)
Time per request:       317.799 [ms] (mean)
Time per request:       31.780 [ms] (mean, across all concurrent requests)
Transfer rate:          55.47 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       5
Processing:    99  318  78.4    310     808
Waiting:       99  317  78.3    310     808
Total:         99  318  78.4    310     808

Percentage of the requests served within a certain time (ms)
  50%    310
  66%    341
  75%    360
  80%    374
  90%    417
  95%    462
  98%    513
  99%    546
 100%    808 (longest request)


# с балансировкой: 10000 запросов
ab -n 10000 -c 10 http://127.0.0.1/api/v2/questions/1
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        nginx/1.19.5
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v2/questions/1
Document Length:        1582 bytes

Concurrency Level:      10
Time taken for tests:   315.589 seconds
Complete requests:      10000
Failed requests:        2
   (Connect: 0, Receive: 0, Length: 2, Exceptions: 0)
Non-2xx responses:      2
Total transferred:      18047038 bytes
HTML transferred:       15817150 bytes
Requests per second:    31.69 [#/sec] (mean)
Time per request:       315.589 [ms] (mean)
Time per request:       31.559 [ms] (mean, across all concurrent requests)
Transfer rate:          55.85 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       4
Processing:     0  315  75.2    309     750
Waiting:        0  315  75.2    308     750
Total:          1  315  75.2    309     750

Percentage of the requests served within a certain time (ms)
  50%    309
  66%    338
  75%    357
  80%    371
  90%    410
  95%    449
  98%    499
  99%    532
 100%    750 (longest request)
