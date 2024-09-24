from datetime import datetime
from typing import Callable


def log_duration(f: Callable, **kwargs):
    start_time = datetime.now()
    output = f(**kwargs)
    end_time = datetime.now()
    print(f'\t\tExecution time: {(end_time - start_time)}s')
    return output