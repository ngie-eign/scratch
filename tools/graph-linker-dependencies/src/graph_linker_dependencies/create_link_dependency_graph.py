#!/usr/bin/env python
"""CLI frontend."""

import argparse
import collections
import pathlib
import re
import subprocess
from collections.abc import Mapping

import pkg_resources
from jinja2 import Environment, FileSystemLoader, select_autoescape

LIBDEPS_CACHE = collections.defaultdict(list)
LDCONFIG_HINT_RE = re.compile(r".+\s+=>\s+(.+)")
NEEDED_SHLIB_RE = re.compile(r".+NEEDED\s+Shared library: \[(.+)\]")


# ruff: noqa: FBT003, S101, S603, S607, T201


def build_library_path_cache() -> Mapping[str, str]:
    ldconfig_hints_map = {}

    all_ldconfig_hints = subprocess.check_output(["ldconfig", "-r"], text=True)
    for ldconfig_hint in all_ldconfig_hints.splitlines(keepends=False):
        matches = LDCONFIG_HINT_RE.match(ldconfig_hint)
        if matches is None:
            continue

        so_full = so_split = matches.group(1)
        ldconfig_hints_map[so_full] = so_full

        so_split = pathlib.Path(so_split)
        while True:
            so_short = so_split.name
            ldconfig_hints_map[so_short] = ldconfig_hints_map[so_split] = so_full
            if so_split.stem == ".so":
                break

    return ldconfig_hints_map


def find_library_dependencies(
    library_: str,
    ldconfig_hints_map: Mapping[str, str],
    libdep_cache: Mapping[str, str],
) -> None:
    if library_ in libdep_cache:
        return

    lib_path = ldconfig_hints_map[library_]

    readelf_lines = subprocess.check_output(["readelf", "-d", lib_path], text=True)
    for readelf_line in readelf_lines.splitlines(False):
        matches = NEEDED_SHLIB_RE.match(readelf_line)
        if matches is None:
            continue
        libdep = matches.group(1)
        libdep_cache[library_].append(libdep)
        find_library_dependencies(libdep, ldconfig_hints_map, libdep_cache)


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    parser = argparse.ArgumentParser()
    parser.add_argument("library")
    parser.add_argument("--graph-generator-file")
    parser.add_argument("--graph-output-file")
    args = parser.parse_args(args=argv)

    libdep_cache = collections.defaultdict(list)

    ldconfig_hints_map = build_library_path_cache()

    library_full_path = str(pathlib.Path(args.library).resolve())
    assert library_full_path in ldconfig_hints_map, (
        f"{library_full_path} not found in ldconfig cache"
    )

    find_library_dependencies(library_full_path, ldconfig_hints_map, libdep_cache)

    env = Environment(
        loader=FileSystemLoader(
            pkg_resources.resource_filename(
                "graph_linker_dependencies",
                "templates",
            ),
        ),
        autoescape=select_autoescape(),
    )
    template = env.get_template("libdep_template.pyt")

    library_name = pathlib.Path(args.library).stem
    graph_py_filename = (
        args.graph_generator_file or f"graph_{library_name}_dependencies.py"
    )
    graph_output_file = (
        args.graph_output_file or f"{library_name}_dependencies_graph.png"
    )
    pathlib.Path(graph_py_filename, "w").write_text(
        template.render(
            libdep_cache=libdep_cache,
            output_file=graph_output_file,
        ),
    )
    print(f"Please run {graph_py_filename} on host where python-graphviz is installed.")


if __name__ == "__main__":
    main()
