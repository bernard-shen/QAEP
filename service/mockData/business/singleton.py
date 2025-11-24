def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class MyClass:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone


if __name__ == '__main__':
    a = MyClass("zhangsan222", "159")
    b = MyClass("lisi", "159")
    print(a.name)
    print(b.name)
