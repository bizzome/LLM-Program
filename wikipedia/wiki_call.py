import httpx
import argparse


def wikipedia(q, language="pt"):
    if language not in ["en", "fr", "pt"]:
        language = "pt"

    wikiresponse = httpx.get(
        f"https://{language}.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json",
        },
    )
    data = wikiresponse.json()
    if (
        "query" in data
        and "search" in data["query"]
        and len(data["query"]["search"]) > 0
    ):
        return data["query"]["search"][0]["snippet"]
    else:
        return "No results found."


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help=(
            "Query to search on Wikipedia, e.g. --query 'Python "
            "(programming language)'. Returns the first snippet of the "
            "search result."
        ),
    )
    parser.add_argument(
        "-l",
        type=str,
        default="pt",
        help=(
            "Language of the Wikipedia to search in, e.g. -l 'en' for "
            "English or -l 'pt' for Portuguese. Defaults to 'pt'."
        ),
    )
    args = parser.parse_args()
    return args.query, args.l


if __name__ == "__main__":
    query, language = get_args()
    response = wikipedia(query, language)
    print("RESPONSE TYPE:", type(response))
    print("SNIPPET:", response)
