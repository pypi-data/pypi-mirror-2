# This file is part of beets.
# Copyright 2010, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Simple but robust implementation of generator/coroutine-based
pipelines in Python. The pipelines may be run either sequentially
(single-threaded) or in parallel (one thread per pipeline stage).

This implementation supports pipeline bubbles (indications that the
processing for a certain item should abort). To use them, yield the
BUBBLE constant from any stage coroutine except the last.

In the parallel case, the implementation transparently handles thread
shutdown when the processing is complete and when a stage raises an
exception.
"""
from __future__ import with_statement # for Python 2.5
import Queue
from threading import Thread, Lock
import sys

BUBBLE = '__PIPELINE_BUBBLE__'
POISON = '__PIPELINE_POISON__'

DEFAULT_QUEUE_SIZE = 16

def clear_queue(q):
    """Safely empty a queue."""
    # This very hacky approach to clearing the queue
    # compliments of Tim Peters:
    # http://www.mail-archive.com/python-list@python.org/msg95322.html
    q.mutex.acquire()
    try:
       q.queue.clear()
       q.unfinished_tasks = 0
       q.not_full.notify()
       q.all_tasks_done.notifyAll()
    finally:
       q.mutex.release()

class PipelineError(object):
    """An indication that an exception occurred in the pipeline. The
    object is passed through the pipeline to shut down all threads
    before it is raised again in the main thread.
    """
    def __init__(self, exc_info):
        self.exc_info = exc_info

class PipelineThread(Thread):
    """Abstract base class for pipeline-stage threads."""
    def __init__(self):
        super(PipelineThread, self).__init__()
        self.abort_lock = Lock()
        self.abort_flag = False

    def abort(self):
        """Shut down the thread at the next chance possible.
        """
        with self.abort_lock:
            self.abort_flag = True
            # Empty the channel before poisoning it.

class FirstPipelineThread(PipelineThread):
    """The thread running the first stage in a parallel pipeline setup.
    The coroutine should just be a generator.
    """
    def __init__(self, coro, out_queue):
        super(FirstPipelineThread, self).__init__()
        self.coro = coro
        self.out_queue = out_queue
        
        self.abort_lock = Lock()
        self.abort_flag = False
    
    def run(self):
        while True:
            # Time to abort?
            with self.abort_lock:
                if self.abort_flag:
                    return
            
            # Get the value from the generator.
            try:
                msg = self.coro.next()
            except StopIteration:
                break
            except:
                self.out_queue.put(PipelineError(sys.exc_info()))
                return
            
            # Send it to the next stage.
            self.out_queue.put(msg)
            if msg is BUBBLE:
                continue
        
        # Generator finished; shut down the pipeline.
        self.out_queue.put(POISON)
    
class MiddlePipelineThread(PipelineThread):
    """A thread running any stage in the pipeline except the first or
    last.
    """
    def __init__(self, coro, in_queue, out_queue):
        super(MiddlePipelineThread, self).__init__()
        self.coro = coro
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        # Prime the coroutine.
        self.coro.next()
        
        while True:
            with self.abort_lock:
                if self.abort_flag:
                    return

            # Get the message from the previous stage.
            msg = self.in_queue.get()
            if msg is POISON:
                break
            elif isinstance(msg, PipelineError):
                self.out_queue.put(msg)
                return
            
            # Invoke the current stage.
            try:    
                out = self.coro.send(msg)
            except:
                self.out_queue.put(PipelineError(sys.exc_info()))
                return
            
            # Send message to next stage.
            if out is BUBBLE:
                continue
            self.out_queue.put(out)
        
        # Pipeline is shutting down normally.
        self.out_queue.put(POISON)

class LastPipelineThread(PipelineThread):
    """A thread running the last stage in a pipeline. The coroutine
    should yield nothing.
    """
    def __init__(self, coro, in_queue):
        super(LastPipelineThread, self).__init__()
        self.coro = coro
        self.in_queue = in_queue

    def run(self):
        # Prime the coroutine.
        self.coro.next()

        while True:
            with self.abort_lock:
                if self.abort_flag:
                    return
                
            # Get the message from the previous stage.
            msg = self.in_queue.get()
            if msg is POISON:
                break
            elif isinstance(msg, PipelineError):
                self.exc_info = msg.exc_info
                return
            
            # Send to consumer.
            try:
                self.coro.send(msg)
            except:
                self.exc_info = sys.exc_info()
                return
        
        # No exception raised in pipeline.
        self.exc_info = None

class Pipeline(object):
    """Represents a staged pattern of work. Each stage in the pipeline
    is a coroutine that receives messages from the previous stage and
    yields messages to be sent to the next stage.
    """
    def __init__(self, stages):
        """Makes a new pipeline from a list of coroutines. There must
        be at least two stages.
        """
        if len(stages) < 2:
            raise ValueError('pipeline must have at least two stages')
        self.stages = stages
        
    def run_sequential(self):
        """Run the pipeline sequentially in the current thread. The
        stages are run one after the other.
        """
        # "Prime" the coroutines.
        for coro in self.stages[1:]:
            coro.next()
        
        # Begin the pipeline.
        for msg in self.stages[0]:
            for stage in self.stages[1:]:
                msg = stage.send(msg)
                if msg is BUBBLE:
                    # Don't continue to the next stage.
                    break
    
    def run_parallel(self, queue_size=DEFAULT_QUEUE_SIZE):
        """Run the pipeline in parallel using one thread per stage. The
        messages between the stages are stored in queues of the given
        size.
        """
        queues = [Queue.Queue(queue_size) for i in range(len(self.stages)-1)]
        threads = [FirstPipelineThread(self.stages[0], queues[0])]
        for i in range(1, len(self.stages)-1):
            threads.append(MiddlePipelineThread(
                self.stages[i], queues[i-1], queues[i]
            ))
        threads.append(LastPipelineThread(self.stages[-1], queues[-1]))
        
        # Start threads.
        for thread in threads:
            thread.start()
        
        # Wait for termination.
        try:
            # The final thread lasts the longest.
            threads[-1].join()
        finally:
            # Halt the pipeline in case there was an exception.
            for thread in threads:
                thread.abort()
            for queue in queues:
                clear_queue(queue)
        
        # Make completely sure that all the threads have finished
        # before we return.
        for thread in threads[:-1]:
            thread.join()

        exc_info = threads[-1].exc_info
        if exc_info:
            # Make the exception appear as it was raised originally.
            raise exc_info[0], exc_info[1], exc_info[2]

# Smoke test.
if __name__ == '__main__':
    import time
    
    # Test a normally-terminating pipeline both in sequence and
    # in parallel.
    def produce():
        for i in range(5):
            print 'generating', i
            time.sleep(1)
            yield i
    def work():
        num = yield
        while True:
            print 'processing', num
            time.sleep(2)
            num = yield num*2
    def consume():
        while True:
            num = yield
            time.sleep(1)
            print 'received', num
    ts_start = time.time()
    Pipeline([produce(), work(), consume()]).run_sequential()
    ts_middle = time.time()
    Pipeline([produce(), work(), consume()]).run_parallel()
    ts_end = time.time()
    print 'Sequential time:', ts_middle - ts_start
    print 'Parallel time:', ts_end - ts_middle
    print

    # Test a pipeline that raises an exception.
    def exc_produce():
        for i in range(10):
            print 'generating', i
            time.sleep(1)
            yield i
    def exc_work():
        num = yield
        while True:
            print 'processing', num
            time.sleep(3)
            if num == 3:
               raise Exception()
            num = yield num * 2
    def exc_consume():
        while True:
            num = yield
            #if num == 4:
            #   raise Exception()
            print 'received', num
    Pipeline([exc_produce(), exc_work(), exc_consume()]).run_parallel(1)
