# Testing SSL response time with and without intermediate certificate
Goal: To test the response time of a https server both with and without an intermediate certificate.

## Method
1. Use ```curl```  and the ```-w``` flag to gather stats about a sequence of test runs to measure ssl performance.
2. Store the results in a csv.
3. Run pandas against the results to generate a summary.

## Scripts
### Generate the test data using curl:
This test uses [curl][1]'s `-w` option to record information about the timings of parts of the connection.

```
url=${1:-https://cmp.oxenfor.de}
test_began=$(date +%s)
echo "url,test_began,ssl_verify_result,time_connect,time_appconnect"
seq 10 | xargs -I@ -n1 curl -kso /dev/null -w "${url},${test_began},%{ssl_verify_result},%{time_connect},%{time_appconnect}\n" ${url}
```
the ouput look like this:
```
url,test_began,ssl_verify_result,time_connect,time_appconnect
https://cmp.oxenfor.de,1523545043,0,0.024777,0.085624
https://cmp.oxenfor.de,1523545043,0,0.043194,0.100740
https://cmp.oxenfor.de,1523545043,0,0.020487,0.073757
https://cmp.oxenfor.de,1523545043,0,0.021635,0.078617
https://cmp.oxenfor.de,1523545043,0,0.025631,0.088463
https://cmp.oxenfor.de,1523545043,0,0.034713,0.091297
https://cmp.oxenfor.de,1523545043,0,0.020146,0.077856
https://cmp.oxenfor.de,1523545043,0,0.020469,0.069975
https://cmp.oxenfor.de,1523545043,0,0.020769,0.073596
https://cmp.oxenfor.de,1523545043,0,0.018849,0.067029
```

## Report on the test data using pandas in python
Use [pandas][2] to get a summary of the data captured above.

```#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import datetime


def main():

    # url,test_began,ssl_verify_result,time_connect,time_appconnect
    file = sys.argv[1]
    df = pd.read_csv(file)
    grouped = df.groupby('url')

    print('time_appconnect')
    print(grouped['time_appconnect'].describe(percentiles=[.25, .5, .75, .95]))
    print
    print
    print('time_connect')
    print(grouped['time_connect'].describe(percentiles=[.25, .5, .75, .95]))

if __name__ == "__main__":
    main()
```
    

```
$ python test.py x.csv
time_appconnect
                        count      mean       std       min       25%  \
url
http://cmp.oxenfor.de    10.0  0.000000  0.000000  0.000000  0.000000
https://cmp.oxenfor.de   10.0  0.083025  0.010743  0.073058  0.077032
https://www.google.com   10.0  0.088041  0.011397  0.075998  0.080668

                             50%       75%       95%       max
url
http://cmp.oxenfor.de   0.000000  0.000000  0.000000  0.000000
https://cmp.oxenfor.de  0.078074  0.086326  0.101792  0.106885
https://www.google.com  0.085488  0.089999  0.107708  0.109029
```

## Results 
### Without INT
```
prod,0,0.082918,0.264459
prod,0,0.015411,0.173446
prod,0,0.014735,0.100602
prod,0,0.015495,0.300788
prod,0,0.057729,0.214030
prod,0,0.018075,0.170491
prod,0,0.015098,0.099262
prod,0,0.014760,0.168736
prod,0,0.015277,0.169352
prod,0,0.058410,0.149260
```

### With INT
```
prod,0,0.016125,0.101527
prod,0,0.016035,0.096808
prod,0,0.016235,0.102082
prod,0,0.016063,0.099946
prod,0,0.015818,0.099608
prod,0,0.015653,0.102116
prod,0,0.017554,0.103193
prod,0,0.016034,0.098340
prod,0,0.019052,0.106298
prod,0,0.015832,0.101168
```


[1]: https://curl.haxx.se/docs/manpage.html "Curl documenation"
[2]: https://pandas.pydata.org/ "Pandas"
