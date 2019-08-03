# loopback
Thread manager and decorator for asynchronous background function execution

## Simple usage in code:
```
from loopback import manager, loop
from time import sleep

@loop(manager, interval = 1)
def threaded_function(arg):
    print("running ")
    sleep(arg)
    return 'OK'


while True:
    print(threaded_function(4))
    sleep(1)
```

## Source Code:
* [https://github.com/vpuhoff/loopback](https://github.com/vpuhoff/loopback)

## Travis CI Deploys:
* [https://travis-ci.com/vpuhoff/loopback](https://travis-ci.com/vpuhoff/loopback) [![Build Status](https://travis-ci.com/vpuhoff/loopback.svg?branch=master)](https://travis-ci.com/vpuhoff/loopback)
