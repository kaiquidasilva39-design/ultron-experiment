import requests
from bs4 import BeautifulSoup

USER_AGENT = "ULTRON-EXPERIMENT/0.1"

def fetch(url, timeout=15):
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    return response.text

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return " ".join(soup.stripped_strings)

def research(url):
    html = fetch(url)
    text = extract_text(html)

    return {
        "url": url,
        "text": text[:20000],
        "length": len(text),
    }
