HANDLERS = {}

def parse_message(msg_type: str):
    def decorator(fn):
        HANDLERS[msg_type.lower()] = fn
        return fn
    return decorator
