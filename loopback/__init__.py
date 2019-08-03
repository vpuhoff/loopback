#coding=utf-8
# import pickledb
# #cache = pickledb.load("cache.db", auto_dump=True, sig=True)
import logging
from time import sleep
import time
import functools
from threading import Thread

class ThreadManager(object):
    """ThM (ThreadManager)
    Handles very simple thread operations:
        Creating single-shot threads -> ThM.run(...)
        Creating 'looping per interval' threads -> ThM.run(...) with loop set to True
        Stopping looping threads based on name -> ThM.stop_loop(...)
        Joining all threads into the calling thread ThM.joinall()
        Removing stopped threads from 'running_threads' - > ThM.free_dead()

     
    The class has been designed for very simple operations, mainly
    for programs that need "workers" that mindlessly loop over a function.

    NOTE: Locks,Events,Semaphores etc. have not been taken into consideration
    and may cause unexpected behaviour if used!
     """
    running_threads = []
    cache = {}
    started = []

    def run(self,targetfunc,thname,loop,interval,arglist=[]):
        """Statrs a new thread and appends it to the running_threads list
        along with the specified values.
        Loop and interval needs to be specified even if you dont
        want it to loop over. This is to avoid lot of keyword arguments
        and possible confusion.
        Example of starting a looping thread:
            ThM.run(function,"MyThreadName",True,0.5,[1,2,"StringArguemnt"])

        To stop it, use:
            ThM.stop_loop("MyThreadName")
        Note, a stopped thread cannot be started again!

        Example of a single-shot thread:
            ThM.run(function,"ThreadName",False,0.5,[1,2,"StringArgument"])
            """
        key = thname+str(arglist)

        if key not in self.started:
            th = Thread(target=self._thread_runner_,args=(targetfunc,thname,interval,arglist))
            th.setDaemon(True)
            self.running_threads.append([th,thname,loop])
            th.start()
            self.started.append(key)
            return key
        else:
            return key

    @classmethod
    def free_dead(self):
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for th in self.running_threads[:]:
            if th[0].isAlive() == False:
                self.running_threads.remove(th)

    @classmethod
    def stop_loop(self,threadname):
        """Stops a looping function that was started with ThM.run(...)"""
        for i,thlis in enumerate(self.running_threads):
            if thlis[1] == threadname:
                self.running_threads[i][2] = False
                break
    
    @classmethod
    def joinall(self):
        """Joins all the threads together into the calling thread."""
        for th in self.running_threads[:]:
            while th[0].isAlive():
                sleep(0.1)
            th[0].join()
         #   print "Thread:",th[1],"joined","isalive:",th[0].isAlive() --- Debug stuff

    @classmethod
    def get_all_params(self):
        """Returns parameters from the running_threads list for external manipulation"""
        for thli in self.running_threads:
            yield(thli[0],thli[1],thli[2])


    #This method is only intended for threads started with ThM !
    @classmethod
    def _thread_runner_(self,targetfunc,thname,interval,arglist):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        indx=0
        for thread in self.running_threads[:]:
            if thname == thread[1]:
                break
            indx+=1
        self.cache[thname] = targetfunc(*arglist)
        while self.running_threads[indx][2] == True:
            #print('Execution [{}], args [{}] started'.format(thname, arglist))
            t1 = time.time()
            try:
                self.cache[thname] = targetfunc(*arglist)
            except Exception as e:
                print('Error while execution [{}], args [{}].\r\t\t{}'.format(thname, arglist,str(e)))
                #print('ERROR\t{}\t[{}]\t{}'.format(thname,arglist,str(e)))
            t2 = time.time()
            print('Execution [{}], args [{}] completed: {}'.format(thname, arglist, str(t2-t1)))
            if interval != 0:
                time.sleep(interval)

manager = ThreadManager()

def loop(manager,  debug=False, interval = 60):
    def wrapper(f):
        @functools.wraps(f)
        def fun(*args, **kwargs):
            key = manager.run(f,f.__name__, True, interval, args)
            t1 = time.time()
            if key in manager.cache:
                res = manager.cache[key]
            else:
                res = f(*args, **kwargs)
                manager.cache[key] =res
            t2 = time.time()
            #notify(name,t2-t1)
            if debug:
                print(f.__name__+":\t"+str(t2-t1),args, kwargs)
            else:
                pass
                #print(f.__name__+":\t"+str(t2-t1))
            return res
        return fun
    return wrapper



@loop(manager, interval = 1)
def threaded_function(arg):
    print("running ")
    sleep(arg)
    return 'OK'


if __name__ == "__main__":
    while True:
        print(threaded_function(4))
        sleep(1)
    # thread = Thread(target = threaded_function, args = (10, ), daemon=True)
    # thread.start()
    # thread.join()
    # print("thread finished...exiting")


