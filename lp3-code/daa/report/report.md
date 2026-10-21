<h1 align="center">Merge Sort vs Multithreaded Merge Sort</h1>
<h3 align="center">Design and Analysis of Algorithms (410241) - Mini-Project Report</h3>
<p align="center">Laboratory Practice III (410246)</p>

<hr/>

<h2 align="center">1\. Problem Statement</h2>

Implement merge sort and multithreaded merge sort. Compare the time required by both algorithms. Also analyse the performance of each algorithm for the best case and the worst case.

<h2 align="center">2\. Objectives</h2>

1. Implement merge sort (divide and conquer) and count the comparisons it makes.
2. Implement a multithreaded merge sort in which the two halves are sorted by different threads.
3. Compare the run time of the two versions for different array sizes.
4. Build a best-case, a worst-case and a random input, and analyse both algorithms on each of them.
5. Check the measured comparison counts against the theoretical formulas.

<h2 align="center">3\. Methodology</h2>

**Merge sort.** An array is split into two halves, each half is sorted recursively, and the two sorted halves are merged into one. A merge repeatedly compares the front elements of the two halves and copies the smaller one.

- Recurrence: T(n) = 2T(n/2) + O(n), which gives **O(n log n)** time in every case.
- Space: O(n) for the temporary array used by the merge.
- Merge sort is stable, because equal elements keep their order (`<=` is used when comparing).

**Multithreaded merge sort.** The two recursive calls work on different parts of the array, so they do not depend on each other. The multithreaded version starts a new thread for the left half and sorts the right half in the current thread. After `join()` the two halves are merged. Two limits keep it efficient:

- Threads are created only for the first 3 levels of splitting, so at most 8 parts are sorted at the same time (`THREAD_DEPTH = 3`).
- Parts smaller than 10,000 elements are sorted without creating a thread (`MIN_PARALLEL`), because creating a thread costs more than it saves on small parts.

The final merges near the top of the recursion are still done by one thread each, so the speed-up is limited and depends on the number of cores.

**Cases analysed.** The number of comparisons depends on how the elements are arranged:

| Case | Input | Comparisons in one merge of two halves | Total for n = 2^k |
|---|---|---|---|
| Best | Already sorted: every element of the left half is smaller than the right half | Only the left half is compared (size / 2) | (n / 2) log2 n |
| Random | Random order | In between | about n log2 n - 1.25 n |
| Worst | Elements alternate between the halves (`0 4 2 6 1 5 3 7` for n = 8) | Every element but one is compared (size - 1) | n log2 n - n + 1 |

The worst-case array is built by undoing the merge level by level: the even positions go to the left half and the odd positions to the right half, recursively. Array sizes are powers of two (2^16, 2^18, 2^20, 2^22), so the formulas are exact.

<h2 align="center">4\. Implementation Details</h2>

The program is one C++17 file, `daa/mini_merge_sort.cpp`, using only the standard library (`vector`, `thread`, `chrono`, `algorithm`, `random`).

| Function | Purpose |
|---|---|
| `mergeParts` | Merges two sorted parts of the array through a temporary array and returns the number of comparisons |
| `mergeSort` | Sequential recursive merge sort, returns the comparisons |
| `parallelMergeSort` | Same algorithm, but starts a `std::thread` for the left half down to `THREAD_DEPTH` levels |
| `bestCase`, `randomCase`, `worstCase` | Build the three kinds of input (random uses a fixed seed 42, so every run is the same) |
| `timeSort` | Sorts a copy of the input 3 times, checks that the result is sorted, and keeps the fastest time |

Both threads write to different parts of the array and of the temporary array, so no locks are needed. Time is measured with `std::chrono::steady_clock`, and both versions sort the same input.

**Compile and run**

```
cd lp3-code/daa
g++ -std=c++17 -O2 -pthread mini_merge_sort.cpp -o mini
./mini              # Windows: mini.exe
```

<h2 align="center">5\. Results</h2>

**Test machine:** CPU ______ , ___ cores, ___ GB RAM, compiler ______ (output of `Hardware threads` below).

<p align="center"><img src="screenshots/output.png" width="620" alt="Program output"/></p>
<p align="center"><em>Figure 1: Output of mini_merge_sort.cpp</em></p>

**5.1 Comparisons (the same for both versions, because both do the same merges).**

| n | Best case: theory | Best case: measured | Worst case: theory | Worst case: measured |
|---|---|---|---|---|
| 65,536 (2^16) | 524,288 | ______ | 983,041 | ______ |
| 262,144 (2^18) | 2,359,296 | ______ | 4,456,449 | ______ |
| 1,048,576 (2^20) | 10,485,760 | ______ | 19,922,945 | ______ |
| 4,194,304 (2^22) | 46,137,344 | ______ | 88,080,385 | ______ |

**5.2 Time in milliseconds (best of 3 runs).**

| n | Case | Merge sort | Multithreaded | Speed-up |
|---|---|---|---|---|
| 2^16 | best / random / worst | ___ / ___ / ___ | ___ / ___ / ___ | ___ |
| 2^18 | best / random / worst | ___ / ___ / ___ | ___ / ___ / ___ | ___ |
| 2^20 | best / random / worst | ___ / ___ / ___ | ___ / ___ / ___ | ___ |
| 2^22 | best / random / worst | ___ / ___ / ___ | ___ / ___ / ___ | ___ |

**5.3 Analysis**

- **Comparisons:** the best case makes about half the comparisons of the worst case, and the random case lies in between. The measured values match the formulas in section 3.
- **Time complexity:** all three cases are O(n log n), so the time should grow a little more than 4 times when n grows 4 times. The best case differs from the worst case only by a constant factor, because the copying work is the same in every case and only the number of comparisons changes. Note your own ratios here: ______ .
- **Multithreaded vs sequential:** the multithreaded version is expected to win on large arrays, by less than the number of cores, because the last merges are done by a single thread. For the smallest sizes the gain can be small, because creating threads has a cost. State what you observed: ______ .
- **Space:** both versions use one temporary array of n elements, so the space is O(n).

**Conclusion.** Merge sort has the same O(n log n) running time in the best, random and worst cases. Only the number of comparisons changes, between (n/2) log2 n and n log2 n - n + 1. Sorting the two halves in separate threads reduces the run time on large inputs, and the gain is limited by the sequential merges and the number of cores.
