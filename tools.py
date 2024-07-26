import httpx


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
    return NotImplementedError(f"Google search not implemented yet for {q}")


def calculate(what):
    return eval(what)
