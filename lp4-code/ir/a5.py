"""IR Assignment 5 - Parse XML text, generate a web graph and compute topic-specific page rank.

Problem statement: parse an XML collection of web pages (title, text, outgoing links),
build the web graph, and compute topic-specific (personalised) PageRank where the random
surfer teleports only to pages about the chosen topic. Compare with ordinary PageRank.

New libs used (all standard library): xml.etree.ElementTree (XML parsing).

Input: the XML file named in xml_path (data/pages.xml, 6 pages) is parsed; ordinary PageRank
and PageRank biased to the topic "sports" are printed side by side.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

# XML file (relative to this folder, a full path also works)
xml_path = "data/pages.xml"


def parse(path):
    """Return (titles, topics, graph) from the XML file."""
    root = ET.parse(Path(__file__).parent / path).getroot()
    titles, topics, graph = {}, {}, {}
    for page in root.findall("page"):
        pid = page.get("id")
        titles[pid] = page.findtext("title")
        topics[pid] = page.findtext("topic")
        graph[pid] = [link.text for link in page.findall("link")]
    return titles, topics, graph


def pagerank(graph, teleport, d=0.85, iterations=100):
    """PageRank where teleport[p] is the probability of jumping to page p."""
    rank = dict(teleport)
    for _ in range(iterations):
        dangling = sum(rank[p] for p in graph if not graph[p])
        new = {p: (1 - d) * teleport[p] + d * dangling * teleport[p] for p in graph}
        for p, outs in graph.items():
            for q in outs:
                new[q] += d * rank[p] / len(outs)
        rank = new
    return rank


def main():
    titles, topics, graph = parse(xml_path)
    n = len(graph)
    print(f"Parsed {n} pages, {sum(len(v) for v in graph.values())} links. Web graph:")
    for p, outs in graph.items():
        print(f"  {p} ({topics[p]}) -> {outs}")

    topic = "sports"
    on_topic = [p for p in graph if topics[p] == topic]
    normal = pagerank(graph, {p: 1 / n for p in graph})
    specific = pagerank(graph, {p: (1 / len(on_topic) if p in on_topic else 0) for p in graph})

    print(f"\n{'Page':<5}{'Title':<22}{'Topic':<12}{'PageRank':>9}{'Topic-specific (' + topic + ')':>26}")
    for p in sorted(graph, key=lambda x: -specific[x]):
        print(f"{p:<5}{titles[p]:<22}{topics[p]:<12}{normal[p]:>9.4f}{specific[p]:>26.4f}")


if __name__ == "__main__":
    main()
