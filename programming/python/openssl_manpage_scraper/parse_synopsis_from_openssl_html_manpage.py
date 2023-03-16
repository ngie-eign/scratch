#!/usr/bin/env python3
"""Scrape library manpage output from OpenSSL.org.
"""

import argparse
import html
import logging
import os
import pathlib
import re
import subprocess
from typing import Optional

import bs4


INCLUDE_RE = re.compile(r"#include <openssl/")
FLATTEN_DECLARATIONS_RE = re.compile(",\n", re.M)
BS4_PARSER = "html5lib"


def parse_args(argv : Optional[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("output", type=argparse.FileType("w"))

    return parser.parse_args(args=argv)


def fetch_manpage_html_text(url: str) -> str:
    import requests
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def extract_synopsis_from_manpage_html(text: str) -> str:
    soup = bs4.BeautifulSoup(text, BS4_PARSER)
    for elem in soup.body.find_all("pre"):
        code_elems = elem.find_all("code")
        if not code_elems or len(code_elems) != 1:
            continue
        synopsis_text = html.unescape(code_elems[0].text.lstrip())
        if INCLUDE_RE.match(synopsis_text) is None:
            synopsis_text = INCLUDE_RE.sub("", synopsis_text)
        return FLATTEN_DECLARATIONS_RE.sub(", ", synopsis_text)


BINDIR = os.path.dirname(__file__)

def main(argv : Optional[str] = None) -> None:
    args = parse_args(argv)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Will parse synopsis from %s", args.url)

    url_path = pathlib.Path(args.url)
    try:
        text = (
            url_path.read_text() if url_path.exists()
            else fetch_manpage_html_text(args.url)
        )
        synopsis = extract_synopsis_from_manpage_html(text)
        if not synopsis:
            raise AssertionError(f"{args.url} has no synopsis")
        with args.output as output_fp:
            output_fp.write(synopsis)
        subprocess.check_call(["clang-format", "-i", f"--style=file:{BINDIR}/.clang_format", output_fp.name])
    except AssertionError as exc:
        print(exc)
        os.unlink(args.output.name)
    except Exception:
        logging.exception("")
        os.unlink(args.output.name)

    logging.debug("Parsed synopsis from %s into %s", args.url, args.output.name)


if __name__ == "__main__":
    main()
