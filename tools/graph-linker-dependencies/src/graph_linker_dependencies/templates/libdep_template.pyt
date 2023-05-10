#!/usr/bin/env python

try:
    import graphviz
except ImportError:
    warnings.warn("This script requires python-graphviz")
    raise

dot = graphviz.Digraph("libdependencies-graph", comment="Library Dependencies Graph")

{% for library, dependencies in libdep_cache.items() %}dot.node("{{library}}")
{% for dependency in dependencies %}dot.edge("{{library}}", "{{dependency}}")
{% endfor %}{% endfor %}
dot.render(format="png", outfile="{{output_file}}")
