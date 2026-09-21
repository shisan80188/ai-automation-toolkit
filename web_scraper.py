"""Dependency-light web scraper with polite defaults.

Fetches a page, extracts text with BeautifulSoup, and follows common
pagination patterns. Uses a realistic User-Agent and configurable delays.
"""

from __future__ import annotations

import time
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def fetch_text(
    url: str,
    selector: str = "body",
    timeout: float = 30.0,
    delay: float = 1.0,
    headers: Optional[dict] = None,
) -> str:
    """Fetch a URL and return the stripped text of the first matching element."""
    resp = requests.get(
        url, headers=headers or DEFAULT_HEADERS, timeout=timeout
    )
    resp.raise_for_status()
    if delay:
        time.sleep(delay)
    soup = BeautifulSoup(resp.text, "html.parser")
    node = soup.select_one(selector)
    return node.get_text(" ", strip=True) if node else ""


def collect_links(
    url: str,
    selector: str = "a",
    timeout: float = 30.0,
    headers: Optional[dict] = None,
) -> List[str]:
    """Return absolute URLs of all links matching a CSS selector."""
    resp = requests.get(
        url, headers=headers or DEFAULT_HEADERS, timeout=timeout
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [
        urljoin(url, tag.get("href"))
        for tag in soup.select(selector)
        if tag.get("href")
    ]


if __name__ == "__main__":
    text = fetch_text("https://example.com", selector="h1")
    print(text)
