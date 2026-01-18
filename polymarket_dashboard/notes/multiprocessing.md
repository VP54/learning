okay# Concurrent.futures
- Python package to asynchronously execute callables.

## ThreadPoolExecutor
- In separate threads execute calls asynchronously.
- All threads are enqueued and joined before exit.

- You have collection of threads
- once one thread does its job its then returned back to the ThreadPool
- To not spinup new threads 
- To cap amount of threads (every thread needs its stack (memory))
- Ensures consistent performance of system

### Description:
- Share memory
- Python code can’t run CPU-bound Python code in parallel because of the GIL
- But I/O (network, DB writes, HTTP requests) releases the GIL, so threads are fine



### Examples:
```python
    def do_something(args): ...

    from concurrent.futures import ThreadPoolExecutor
    lst = [1, 2, 3, 4, 5]
    executor = ThreadPoolExecutor(max_workers=10)
    with executor as _executor:
        future_url = {_executor.submit(do_something, i): i for i in lst}
        
```

## ProcessPoolExecutor

### Description:

- Each process has its own Python interpreter → runs truly in parallel
- Separate memory → no GIL contention
- Communication via multiprocessing.Queue, pipes, or other IPC

