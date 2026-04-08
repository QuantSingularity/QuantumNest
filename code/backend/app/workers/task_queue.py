import secrets
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()

# In-process task result store (replaces Redis/Celery backend in dev/test)
_task_store: Dict[str, Any] = {}


class MockTaskResult:
    """Mimics a Celery AsyncResult – can be created from a completed task or looked up by id."""

    def __init__(self, task_id_or_result: Any = None):
        # If called with a string that looks like a stored task id, look it up
        if isinstance(task_id_or_result, str) and task_id_or_result in _task_store:
            self.id = task_id_or_result
            self._result = _task_store[task_id_or_result]
            self.status = "SUCCESS"
        elif isinstance(task_id_or_result, str):
            # Unknown task id – treat as pending/unknown
            self.id = task_id_or_result
            self._result = None
            self.status = "PENDING"
        else:
            # Created from a completed execution result
            self.id = secrets.token_hex(16)
            self._result = task_id_or_result
            self.status = "SUCCESS"
            _task_store[self.id] = self._result

    def ready(self) -> bool:
        return self.status in ("SUCCESS", "FAILURE")

    def successful(self) -> bool:
        return self.status == "SUCCESS"

    @property
    def result(self) -> Any:
        return self._result


class MockCeleryTask:
    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs) -> MockTaskResult:
        result = self.func(*args, **kwargs)
        return MockTaskResult(result)

    def apply_async(self, args=None, kwargs=None, **options) -> MockTaskResult:
        result = self.func(*(args or []), **(kwargs or {}))
        return MockTaskResult(result)


class MockCeleryApp:
    def task(self, **kwargs) -> Any:
        def decorator(func):
            return MockCeleryTask(func)

        return decorator

    def conf(self):
        pass


celery_app = MockCeleryApp()
