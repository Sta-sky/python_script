from functools import wraps


def singtelon(cls):
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return get_instance


@singtelon
def parse():
    pass


print(parse.__doc__)
print(parse.__name__)

