import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

USER_AGENT = "ULTRON-EXPERIMENT/2.0"

def search_web(query, limit=5):
    url = "https://www.google.com/search?q=" + quote(query)

    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.select("a"):
        href = link.get("href", "")
        title = link.get_text(" ", strip=True)

        if href.startswith("http") and title:
            results.append({
                "title": title,
                "url": href,
            })

        if len(results) >= limit:
            break

    return results
