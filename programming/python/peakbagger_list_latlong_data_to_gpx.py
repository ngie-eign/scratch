#!/usr/bin/env python
"""Peakbagger GPX data exporter.
"""

import argparse
import concurrent.futures
import logging
import re
import urllib.parse

import bs4
import gpxpy.gpx
import requests


argparser = argparse.ArgumentParser()
argparser.add_argument("--output-file", default="exported.gpx")
argparser.add_argument("url")

args = argparser.parse_args()


ASCENT_LIST_FILTER = (
    "Peak",
    "Ascent Date",
)

BS4_PARSER = "html5lib"


LAT_LONG_RE = re.compile(
    r'(?P<latitude>[^"]+), (?P<longitude>[^,]+) \(Dec Deg\)',
    re.DOTALL,
)


def get_html_text(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def make_waypoint(name, latitude, longitude):
    return gpxpy.gpx.GPXWaypoint(latitude=latitude, longitude=longitude, name=name)


def get_lat_long_from_peak_page(url):
    text = get_html_text(url)
    soup = bs4.BeautifulSoup(text, BS4_PARSER)

    for lat_long_elem in soup.body.find(id="Form1").find_all("td"):
        for string in lat_long_elem.stripped_strings:
            match = LAT_LONG_RE.search(string)
            if match is None:
                continue
            return match.groupdict()

    return None


def get_list_of_ascents_from_ascent_list(url):
    text = get_html_text(url)
    soup = bs4.BeautifulSoup(text, BS4_PARSER)

    rank_anchor = soup.body.find(id="Form1").find("th", string="Rank")
    if rank_anchor is None:
        return

    ascent_header_row = rank_anchor.parent
    ascent_header_mapping = {
        i: ascent_header_elem.text
        for i, ascent_header_elem in enumerate(ascent_header_row.find_all("th"))
        if ascent_header_elem.text in ASCENT_LIST_FILTER
    }

    peak_links = {}
    peaks_not_climbed = []

    ascent_table = ascent_header_row.parent
    for i, ascent_row in enumerate(ascent_table.find_all("tr")):
        if ascent_row.find("th") or not ascent_row.text.strip():
            continue
        peak_ascent_data = {
            ascent_header_mapping[j]: ascent_col
            for j, ascent_col in enumerate(ascent_row.children)
            if j in ascent_header_mapping
        }
        peak_name = peak_ascent_data["Peak"].text.strip()
        peak_climbed = bool(peak_ascent_data["Ascent Date"].text.strip())
        if peak_climbed:
            logging.debug(f"Skipping {peak_name}; already climbed.")
            continue

        peak_link = urllib.parse.urljoin(
            url, peak_ascent_data["Peak"].find("a").get("href")
        )
        peak_links[peak_name] = peak_link

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_peaks = {
            executor.submit(get_lat_long_from_peak_page, peak_link): peak_name
            for peak_name, peak_link in peak_links.items()
        }

        for i, future in enumerate(concurrent.futures.as_completed(future_to_peaks), 1):
            peak_name = future_to_peaks[future]
            peak_def = future.result()
            waypoint = make_waypoint(
                peak_name, peak_def["latitude"], peak_def["longitude"]
            )
            logging.info("[%02d/%02d] waypoints created.", i, len(peak_links))
            peaks_not_climbed.append(waypoint)

    return peaks_not_climbed


gpx = gpxpy.gpx.GPX()

peaks_not_climbed = get_list_of_ascents_from_ascent_list(args.url)

gpx.waypoints.extend(peaks_not_climbed)

with open(args.output_file, "w") as fp:
    fp.write(gpx.to_xml())
