"""IR Assignment 2 - Implement the PageRank algorithm.

Problem statement: rank web pages by importance from the link structure using the
iterative PageRank formula PR(p) = (1-d)/N + d * sum(PR(q)/out(q)) over pages q that
link to p, with damping factor d = 0.85 and handling of dangling pages.

New libs used: none (pure Python standard library).

Input: the web graph is read from graph_path (data/graph.txt, one line per page like
'A: B C') and ranked by power iteration until convergence.
"""

from pathlib import Path

# graph file (relative to this folder, a full path also works)
graph_path = "data/graph.txt"


def read_graph(path):
    """Read lines like 'A: B C' into {page: [pages it links to]}."""
    graph = {}
    for line in (Path(__file__).parent / path).read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            page, _, links = line.partition(":")
            graph[page.strip()] = links.split()
    return graph


def pagerank(graph, d=0.85, tol=1e-8, max_iter=100):
    pages = list(graph)
    n = len(pages)
    rank = {p: 1 / n for p in pages}
    for iteration in range(1, max_iter + 1):
        # rank of dangling pages is shared equally among all pages
        dangling = sum(rank[p] for p in pages if not graph[p])
        new = {p: (1 - d) / n + d * dangling / n for p in pages}
        for p in pages:
            for target in graph[p]:
                new[target] += d * rank[p] / len(graph[p])
        converged = sum(abs(new[p] - rank[p]) for p in pages) < tol
        rank = new
        if converged:
            break
    return rank, iteration


def main():
    graph = read_graph(graph_path)
    rank, iterations = pagerank(graph)
    print(f"Converged in {iterations} iterations (sum of ranks = {sum(rank.values()):.4f})")
    for position, (page, score) in enumerate(sorted(rank.items(), key=lambda x: -x[1]), 1):
        print(f"  {position}. page {page}: {score:.4f}  (in-links: {[q for q in graph if page in graph[q]]})")


if __name__ == "__main__":
    main()
