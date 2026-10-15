"""Assignment 3 - Implement basic logic gates using Hebbnet neural networks.

Problem statement: use the Hebb rule (w_i = w_i + x_i * t, b = b + t) with bipolar
inputs/targets (+1 / -1) to learn AND, OR, NAND and NOR, and show that XOR cannot be
learned by a single Hebb neuron.
Libraries: none (pure Python, standard library only).
Driver: trains each gate on its truth table, prints weights, bias and a check table.
"""

INPUTS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]   # bipolar: 1 = true, -1 = false

GATES = {                                         # target for each of the 4 input rows
    "AND": [1, -1, -1, -1],
    "OR": [1, 1, 1, -1],
    "NAND": [-1, 1, 1, 1],
    "NOR": [-1, -1, -1, 1],
    "XOR": [-1, 1, 1, -1],
}


def train_hebb(inputs, targets):
    """One pass over the patterns: w += x * t and b += t (starting from zero)."""
    w, b = [0, 0], 0
    for x, t in zip(inputs, targets):
        w = [wi + xi * t for wi, xi in zip(w, x)]
        b += t
    return w, b


def activation(net):
    return 1 if net > 0 else -1 if net < 0 else 0   # 0 means the net cannot decide


def main():
    for name, targets in GATES.items():
        w, b = train_hebb(INPUTS, targets)
        print(f"\n{name} gate: weights = {w}, bias = {b}")
        print("  x1  x2 | target | net | output")
        correct = 0
        for x, t in zip(INPUTS, targets):
            net = b + sum(wi * xi for wi, xi in zip(w, x))
            out = activation(net)
            correct += out == t
            print(f"  {x[0]:>2}  {x[1]:>2} | {t:>5}  | {net:>3} | {out:>5}")
        print(f"  Learned correctly: {correct == 4}  ({correct}/4 rows right)")
    print("\nXOR is not linearly separable, so a single Hebb neuron cannot learn it.")


if __name__ == "__main__":
    main()
