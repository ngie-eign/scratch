#!/usr/bin/env python3
"""Scrape library manpage listing from OpenSSL.org.
"""

import argparse
import urllib.parse
from typing import Optional

import bs4
import requests


BS4_PARSER = "html5lib"


def parse_args(argv : Optional[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")

    return parser.parse_args(args=argv)


def get_manpage_html_text(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def extract_libcall_links_from_page(text: str) -> str:
    soup = bs4.BeautifulSoup(text, BS4_PARSER)
    return [
        link["href"] for link in soup.body.article.table.tbody.find_all("a", href=True)
    ]


def main(argv : Optional[str] = None) -> None:
    args = parse_args(argv)
    text = get_manpage_html_text(args.url)
    parsed_links = extract_libcall_links_from_page(text)
    for link in parsed_links:
        print(urllib.parse.urljoin(args.url, link))


if __name__ == "__main__":
    main()
