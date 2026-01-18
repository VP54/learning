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


# QuestDB

## Types:

- **SYMBOL**
  - like enum, for strings that repeat often
  - stored separately from the column data. Represented as an integer under the hood.

# Design patterns
- *Problems I met and what I used instead*

## Routing messages in a Queue
- I needed to route messages to separate parsers from queue.
  - To solve this I could:
    - match - case it
    - Strategy it
      ```python
      from abc import ABC
      
      class Handler(ABC):
          def handle(self, payload, logger): ...
    
      class BinanceHandler(): ...
      class PolymarketHandler(): ...
      
      HANDLERS = {
          "binance": BinanceHandler(),
          "polymarket": PolymarketHandler(),
      }
    
      def route_message((msg_type, payload), logger):
          HANDLERS[msg_type.lower()].handle(payload, logger)
      ```
    - Register it
      ```python
        HANDLERS = {}
        
        def register(msg_type: str):
            def deco(fn):
                HANDLERS[msg_type.lower()] = fn
                return fn
            return deco
        
        @register("binance")
        def handle_binance(payload, logger):
            ...
        
        def route_message((msg_type, payload), logger):
            HANDLERS[msg_type.lower()](payload, logger)

      ```
### Choice
- Choice was made to limit if-else segments and learn a bit about different design patterns.

#### Match - Case
- Good for very simple logic
- Not ideal for multiple sources

#### Strategy
- **Good**
  - Good OOP pattern
- 
- **Bad**
- Can become complex
  - Introduces abstract classes etc.

#### Register
- **Good**
  - Simple interface w/o overhead
  - Can be scaled using decorators

- **Bad**
  - Parsers have to be initialized

# Looping in python

- The problem
```python
    bids = [{"price": "0.4", "size": "100"}, ...]
    asks = [{"price": "0.5", "size": "100"}, ...]

    bid_sizes = [float(i['size']) for i in bids]
    bid_prices = [float(i['price']) for i in bids]
    asks_sizes = [float(i['size']) for i in asks]
    asks_prices = [float(i['price']) for i in asks]
```
- Quite expensive to do 4 loops based on the fact that:
  - fetch next element
  - assign to i
  - i['price'] -> hashmap lookup
  - lookup `float` (retype)
  - call `float(...)`
  - lookup `.append`
  - call `.append(...)`

- So the possible room to make it faster is:
  - faster lookup binding
    - make the lookup before as local
    - lookups happen in (local -> global -> builtins)
  - not as many element fetching
    - less iterations -> less fetching of elements
    - less assigning to i


