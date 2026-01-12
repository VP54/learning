# Concurrent.futures
- Python package to asynchronously execute callables.

## ThreadPoolExecutor
- In separate threads execute calls asynchronously.
- All threads are enqueued and joined before exit.

- You have collection of threads
- once one thread does its job its then returned back to the ThreadPool
- To not spinup new threads 
- To cap amount of threads (every thread needs its stack (memory))
- Ensures consistent performance of system

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