# Table of Contents
1. [Asyncio](#Asyncio)
2. [Running code](#Running code)
3. [Third Example](#third-example)
4. [Fourth Example](#fourth-examplehttpwwwfourthexamplecom)

# Asyncio
Asyncio is a module for asynchronous communication.

## Functions:
- Some notes on different functions.

## Types

#### asyncio.Task
- Future-like object that runs code
- not tread-safe
- used to run coroutines in an event loop
- If coroutine (Task) is awaiting on a Future, task then suspends other execution and waits on Future.
- While Task awaits on a Future, the event loop runs other Tasks, callbacks and IO operations.

## Creating tasks:

### asyncio.create_task
- Wrap the coro coroutine into a Task and schedule its execution

### asyncio.TaskGroup.create_task

## Separating workflow to multiple threads
- to not block event loop execution I can put some blocking operation (I/O, logging, file handling) to a separate loop.

### asyncio.to_thread
- async asyncio.to_thread(func, /, *args, **kwargs)

## Running code

- Every code is run in an event loop. (default is ThreadPoolExecutor)

**Blocking IO:**
- Blocking operations need to be run in separate thread. Otherwise can be blocking
  - Use ThreadPoolExecutor

**Example**:
- file operations

**CPU-bound operations:**
- Blocks the event loop
  - run in ProcessPool

**Example:**
- number operations
  - parsing operations

    ```python
    loop = asyncio.get_running_loop()  
    result = await loop.run_in_executor(
          None, blocking_io)
      print('default thread pool', result)

      # 2. Run in a custom thread pool:
      with concurrent.futures.ThreadPoolExecutor() as pool:
          result = await loop.run_in_executor(
              pool, blocking_io)
          print('custom thread pool', result)

      # 3. Run in a custom process pool:
      with concurrent.futures.ProcessPoolExecutor() as pool:
          result = await loop.run_in_executor(
              pool, cpu_bound)
          print('custom process pool', result)

      # 4. Run in a custom interpreter pool:
      with concurrent.futures.InterpreterPoolExecutor() as pool:
          result = await loop.run_in_executor(
              pool, cpu_bound)

    ```



