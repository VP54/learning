# Python Built-in function

```python
```

## Link:
[Built-in](https://docs.python.org/3/library/functions.html)


## Built-in functions

- **any**
    - returns True if any element of an iterable is True
        ```python
        any([False, False])     # False
        any([True, False])      # True
        ```

- **classmethod**
    - decorator that converts class function in classmethod.
    - Usage as to control behavior of the whole class/child classes (config, rate limiting)
        ```python
        from dataclass import dataclass        

        @dataclass(frozen=True)
        class PostgresLoadConfig:
            dsn: str
            table: str
            batch_size: int = 1000

        class PostgresLoader(Loader):
            @classmethod
            def from_env(cls):
                return cls(
                    PostgresLoadConfig(
                        dsn=os.getenv("PG_DSN"),
                        table=os.getenv("PG_TABLE"),
                    )
                )
        ```

- **enumerate(iterable, start=0)**
    - creates iterable tuple with (index, element)
        ```python
            iterable = ["a", "b"]
            list(enumerate(iterable))  # [(0, "a"), (1, "b")]
        ```

- **filter(iterable, function)**
    - equivalent to:
        ```python
            [i for i in iterable if function(i)]
        ```

- **getattr** x **setattr** x **hasattr**
    - getattr:
        ```python 
            x = {"a": 1}
            getattr("a") = 1  # equivalent x.a
        ```

    - hasattr(object, name):
        - applies getattr to object and name. Returns bool
        ```python 
            x = {"a": 1}
            if hasattr(x, "a"):
                ...
            else:
                ...
        ```

## Deep Copy x Shallow Copy

### Deep Copy:

- It will first construct a new collection object and then recursively populate it with copies of the child objects found in the original.
    ```python
        import copy

        a = [[1, 2, 3], [4, 5, 6]]

        b = copy.deepcopy(a)

        b[0][0] = 99 
        print(a)  # [[1, 2, 3], [4, 5, 6]]
        print(b)  # [[99, 2, 3], [4, 5, 6]]
    ``` 

### Shallow Copy:
- A shallow copy creates a new object but retains references to the objects contained within the original. It only copies the top-level structure without duplicating nested elements.
    ```python
        import copy

        a = [[1, 2, 3], [4, 5, 6]]

        b = copy.deepcopy(a)

        b[0][0] = 99 
        print(a)  # [[99, 2, 3], [4, 5, 6]]
        print(b)  # [[99, 2, 3], [4, 5, 6]]

        # But works in the other way too.
        a[0][0] = 99 
        print(a)  # [[99, 2, 3], [4, 5, 6]]
        print(b)  # [[99, 2, 3], [4, 5, 6]]
    ``` 

