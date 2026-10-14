"""IR Assignment 5 - Parse XML text, generate a web graph and compute topic-specific page rank.

Problem statement: parse an XML collection of web pages (title, text, outgoing links),
build the web graph, and compute topic-specific (personalised) PageRank where the random
surfer teleports only to pages about the chosen topic. Compare with ordinary PageRank.

New libs used (all standard library): xml.etree.ElementTree (XML parsing).

Driver: an embedded XML of 6 pages is parsed; ordinary PageRank and PageRank biased to
the topic "sports" are printed side by side. No input is taken at runtime.
"""

import xml.etree.ElementTree as ET

XML_DATA = """
<pages>
  <page id="p1"><title>Cricket World Cup</title><topic>sports</topic>
    <text>India wins the cricket match</text><link>p2</link><link>p5</link></page>
  <page id="p2"><title>Football League</title><topic>sports</topic>
    <text>Goals and football fans</text><link>p1</link></page>
  <page id="p3"><title>Stock Market News</title><topic>finance</topic>
    <text>Sensex rises as markets rally</text><link>p1</link><link>p4</link></page>
  <page id="p4"><title>Banking Update</title><topic>finance</topic>
    <text>Interest rates and loans</text><link>p3</link></page>
  <page id="p5"><title>Olympic Games</title><topic>sports</topic>
    <text>Athletes and medals</text><link>p1</link><link>p2</link></page>
  <page id="p6"><title>Tech Gadgets</title><topic>technology</topic>
    <text>New phones launched</text><link>p3</link><link>p1</link></page>
</pages>
"""


def parse(xml_text):
    """Return (titles, topics, graph) from the XML document."""
    root = ET.fromstring(xml_text)
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
    titles, topics, graph = parse(XML_DATA)
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
