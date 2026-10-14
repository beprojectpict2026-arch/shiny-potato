# LP3 (410246) - Laboratory Practice III

| Folder | Subject | Language / tool | How to run |
|---|---|---|---|
| `daa/` | Design and Analysis of Algorithms (A1-A5 + mini-project: Naive vs Rabin-Karp) | C++17 | `g++ -std=c++17 -O2 a1.cpp -o a1` then `./a1` (Windows: `a1.exe`) |
| `ml/` | Machine Learning (B1-B5 + mini-project: Titanic survival) | Jupyter notebooks, Python | `uv sync` then `uv run jupyter lab`, open a notebook, *Run All* |
| `bt/` | Blockchain Technology (C1-C5 + mini-project: e-voting) | Solidity, Remix IDE, MetaMask | Open the `.sol` file in [Remix](https://remix.ethereum.org), compile, deploy; see the guides |

## Notes

- **DAA:** every `.cpp` file has a header comment (problem statement, libraries, driver) and takes no input at runtime. No C++ compiler? Use MinGW-w64/MSYS2 on Windows, or paste a file into an online compiler.
- **ML:** the Kaggle datasets are not bundled. Each notebook generates synthetic data with the same columns so it runs anywhere; to use the real CSV, set `CSV_PATH` in the first code cell. Saved outputs in the notebooks come from the synthetic data, so the scores will differ from real-data results.
- **BT:** no Solidity compiler install is needed, because Remix has it built in. C1, C4, C5 and the mini-project guide are write-ups; C2, C3 and the mini-project are contracts. Use the **Sepolia** test network (the manual's Rinkeby/Kovan/Ropsten are shut down).
