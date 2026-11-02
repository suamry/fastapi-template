# encoding: utf-8
from threading import Lock


class SingletonMeta(type):
    """线程安全单例模式"""
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


if __name__ == '__main__':
    # 演示代码
    class SingletonOss(metaclass=SingletonMeta):
        instance: object

        def __init__(self, instance) -> None:
            print("init")
            self.instance = instance

    test_1 = SingletonOss({"zhangsan": 18}).instance
    print(id(test_1), test_1)

    test_2 = SingletonOss({"zhangsan": 19}).instance
    print(id(test_2), test_2)
