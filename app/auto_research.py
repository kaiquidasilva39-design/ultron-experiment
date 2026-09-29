import requests


def search_public_knowledge(query):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": 3,
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
        headers={"User-Agent": "ULTRON-EXPERIMENT/1.0"},
    )
    response.raise_for_status()

    data = response.json()

    return [
        {
            "title": item["title"],
            "snippet": item["snippet"],
        }
        for item in data.get("query", {}).get("search", [])
    ]
