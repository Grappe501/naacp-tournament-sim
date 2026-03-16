from contextlib import contextmanager
from .engine import engine

@contextmanager
def transaction():

    with engine.begin() as conn:
        yield conn
