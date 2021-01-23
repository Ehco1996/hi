# hi

hi is a tiny cli program that send benchmark request to "almost" everything. note that it's inspired by [rakyll/hey](https://github.com/rakyll/hey) and implemented by python/asyncio

## Install

 `pip install py-hi`

## Usage

* say hi to github

 `hi https://github.com`

* you will see

``` bash
➜ hi https://github.com

Send request to https://github.com

Summary:
Total:          6.327 secs
Slowest:        6.297 secs
Fastest:        1.447 secs
Average:        4.388 secs
Requests/sec:   31.611

Status code distribution:
[200]        200 responses
```

## TODO

* more send flag
* request benchmark through shadowsocks
