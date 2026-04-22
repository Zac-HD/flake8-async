# 3rd-party context managers with internal cancel scopes are detected
# regardless of the base library.
from contextlib import asynccontextmanager, contextmanager

import httpx


async def foo_httpx_async_client():
    async with httpx.AsyncClient() as _:
        yield 1  # error: 8


async def foo_httpx_client():
    with httpx.Client() as _:
        yield 1  # error: 8


@asynccontextmanager
async def foo_httpx_async_client_contextmanager():
    async with httpx.AsyncClient() as _:
        yield 1  # safe


@contextmanager
def foo_httpx_client_contextmanager():
    with httpx.Client() as _:
        yield 1  # safe


# Only httpx.AsyncClient / httpx.Client are special-cased; other httpx calls
# aren't treated as cancel-scope CMs.
async def foo_httpx_other():
    with httpx.Unrelated() as _:  # type: ignore[attr-defined]
        yield 1  # safe
