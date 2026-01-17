# Asyncio threads

- Every socket connection is run in a thread. Meaning 2 scrapers + 1 worker == 3 threads. (normally)
- Asyncio can handle multiple socket connections with non-blocking I/O

## Non-blocking x Blocking process
- non-blocking process: The operation yields control so other tasks can run while waiting. 
  - usually this means process returns some Task, Future.
  - asyncio

- blocking process: The current thread cannot do anything else until the operation completes.

## Queues
- asyncio.Queue and queue.Queue can hold any Python object.
- multiprocessing.Queue requires objects to be pickleable.
  - This means those object just contain simple data: `dict`, `list`, `tuple`, `str`, `int`, `float`, `bytes`
- Pickleable objects are usually simple data structures or properly defined classes.

# Docker
- To create a Quest DB use: `docker compose up`

# QuestDB

## Types:

- **SYMBOL**
  - like enum, for strings that repeat often
  - stored separately from the column data. Represented as an integer under the hood.



    