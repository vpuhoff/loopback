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