import importation  # noqa: 401


def test_httpx():
    import httpx  # type: ignore

    print("module resolved at", httpx.__file__)
