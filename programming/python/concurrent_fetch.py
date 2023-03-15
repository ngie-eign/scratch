#!/usr/bin/env python3

import argparse
import concurrent.futures
import logging
import os
import pathlib
import sys
from typing import Optional

import requests


# pylint: disable=useless-return

def fetch(
    output_dir: pathlib.Path, url: str, retries: int, timeout: Optional[float]
) -> None:
    dest_path = str(output_dir / os.path.basename(url))

    logging.debug("Will fetch %r -> %r with timeout=%r.", url, dest_path, timeout)

    for try_left in range(retries - 1, -1, -1):
        try:
            resp = requests.get(url, stream=True, timeout=timeout)
            resp.raise_for_status()
            with open(dest_path, "w") as output_fp:
                output_fp.write(resp.text)
        except (requests.ConnectionError, requests.Timeout):
            if try_left == 0:
                raise
            logging.exception("Fetching %r failed; will try fetching %d more times.", url, timeout)
    return None


def fetch_concurrent(
    output_dir: pathlib.Path,
    urls: list[str],
    retries: int,
    max_workers: Optional[int],
    timeout: Optional[float],
) -> list[str]:
    failed_fetches = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_urls = {
            executor.submit(
                fetch, output_dir=output_dir, retries=retries, timeout=timeout, url=url
            ): url
            for url in urls
        }
        for future in concurrent.futures.as_completed(future_to_urls):
            url = future_to_urls[future]
            try:
                future.result()
            except Exception:  # pylint: disable=broad-except
                logging.exception("%s did not fetch successfully.", url)
                failed_fetches.append(url)
    return failed_fetches


def main(argv: Optional[list[str]] = None) -> int:
    def positive_number(value: str) -> int:
        int_value = int(value)
        if int_value <= 0:
            raise ValueError("Value must be a positive integer.")
        return int_value

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--max-workers", default=None, type=int)
    argparser.add_argument("--output-dir", required=True)
    argparser.add_argument("--retries", default=1, type=positive_number)
    argparser.add_argument("--timeout", default=None, type=float)
    argparser.add_argument("--verbose", action="store_true", default=False)
    argparser.add_argument("urls", nargs="+")

    args = argparser.parse_args(argv)

    output_dir = pathlib.Path(args.output_dir)
    # output_dir.mkdir(exist_ok=True, parents=True)

    if args.verbose:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        # logging.debug(f"Will fetch {args.urls!r}")

    failed_fetches = fetch_concurrent(
        output_dir=output_dir,
        urls=args.urls,
        retries=args.retries,
        max_workers=args.max_workers,
        timeout=args.timeout,
    )

    # logging.debug(f"Fetched {args.urls!r}")

    return len(failed_fetches)


if __name__ == "__main__":
    sys.exit(main())
