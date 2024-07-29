import httpx
from googlesearch import search


def wikipedia(q):
    return httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json",
        },
    ).json()["query"]["search"][0]["snippet"]


def google_search(q):
    """Returns a list of SearchResult from a Google search.
    Properties:
    - title
    - url
    - description"""
    return list(search(q, advanced=True))


def calculate(what):
    return eval(what)
