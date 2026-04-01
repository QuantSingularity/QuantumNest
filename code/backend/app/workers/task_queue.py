from typing import Any

from dotenv import load_dotenv

load_dotenv()


class MockCeleryTask:
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def apply_async(self, args=None, kwargs=None, **options):
        return self.func(*(args or []), **(kwargs or {}))


class MockCeleryApp:
    def task(self, **kwargs) -> Any:
        def decorator(func):
            return MockCeleryTask(func)

        return decorator

    def conf(self):
        pass


celery_app = MockCeleryApp()
