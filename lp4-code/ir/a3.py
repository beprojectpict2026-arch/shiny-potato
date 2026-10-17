"""IR Assignment 3 - Map-reduce program to count alphabetic characters.

Problem statement: count the occurrences of each alphabetic character in a dataset,
case-insensitive (upper and lower case are merged) and ignoring non-alphabetic
characters, using the map -> shuffle -> reduce model.

New libs used (all standard library): multiprocessing.Pool (parallel map workers),
collections.defaultdict (shuffle/group by key).

Input: the text file named in dataset_path (data/dataset.txt) is split into 3 chunks, mapped
in parallel, shuffled and reduced; the result is cross-checked with collections.Counter.
"""

from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

# dataset file (relative to this folder, a full path also works)
dataset_path = "data/dataset.txt"


def mapper(chunk):
    """Map phase: emit (letter, 1) for every alphabetic character."""
    return [(ch.lower(), 1) for ch in chunk if ch.isalpha()]


def shuffle(mapped_outputs):
    """Shuffle phase: group all emitted values by key."""
    groups = defaultdict(list)
    for pairs in mapped_outputs:
        for key, value in pairs:
            groups[key].append(value)
    return groups


def reducer(item):
    """Reduce phase: sum the values of one key."""
    key, values = item
    return key, sum(values)


def split(text, parts):
    """Split the dataset into roughly equal chunks (the input splits)."""
    size = -(-len(text) // parts)
    return [text[i:i + size] for i in range(0, len(text), size)]


def main():
    dataset = (Path(__file__).parent / dataset_path).read_text(encoding="utf-8")
    chunks = split(dataset, 3)
    with Pool(3) as pool:
        mapped = pool.map(mapper, chunks)
        counts = dict(pool.map(reducer, shuffle(mapped).items()))

    print(f"{len(chunks)} input splits, {sum(len(m) for m in mapped)} (key, 1) pairs emitted")
    for letter in sorted(counts):
        print(f"  {letter}: {counts[letter]}")
    expected = Counter(ch.lower() for ch in dataset if ch.isalpha())
    print("Matches Counter check:", counts == dict(expected))


if __name__ == "__main__":
    main()
