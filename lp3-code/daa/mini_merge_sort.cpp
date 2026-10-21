/*
 * DAA Mini-project - Merge sort vs multithreaded merge sort.
 *
 * Problem statement: implement merge sort and a multithreaded merge sort, compare the time taken by
 * both, and analyse each one for the best case, the worst case and a random (average) input.
 * Libraries used (standard library only): <vector>, <thread>, <chrono>, <algorithm>, <random>, <iostream>.
 *
 * Driver: for array sizes 2^16 to 2^22 it builds a best-case (already sorted), a random and a
 * worst-case (most comparisons) array, sorts each with both versions, checks the result and prints
 * the comparisons and the best of 3 run times. No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 -pthread mini_merge_sort.cpp -o mini && ./mini
 */
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

using namespace std;
using Clock = chrono::steady_clock;
typedef long long ll;

const int THREAD_DEPTH = 3;     // 3 levels of splitting = up to 8 parts sorted at the same time
const int MIN_PARALLEL = 10000; // smaller parts are sorted in the calling thread

ll mergeParts(vector<int>& a, vector<int>& tmp, int lo, int mid, int hi) {
    int i = lo, j = mid, k = lo;
    ll comparisons = 0;
    while (i < mid && j < hi) {
        comparisons++;
        tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    copy(tmp.begin() + lo, tmp.begin() + hi, a.begin() + lo);
    return comparisons;
}

ll mergeSort(vector<int>& a, vector<int>& tmp, int lo, int hi) {
    if (hi - lo < 2) return 0;
    int mid = lo + (hi - lo) / 2;
    ll c = mergeSort(a, tmp, lo, mid) + mergeSort(a, tmp, mid, hi);
    return c + mergeParts(a, tmp, lo, mid, hi);
}

ll parallelMergeSort(vector<int>& a, vector<int>& tmp, int lo, int hi, int depth) {
    if (hi - lo < 2) return 0;
    if (depth == 0 || hi - lo < MIN_PARALLEL) return mergeSort(a, tmp, lo, hi);
    int mid = lo + (hi - lo) / 2;
    ll left = 0;
    thread worker([&] { left = parallelMergeSort(a, tmp, lo, mid, depth - 1); });
    ll right = parallelMergeSort(a, tmp, mid, hi, depth - 1);
    worker.join();
    return left + right + mergeParts(a, tmp, lo, mid, hi);
}

vector<int> bestCase(int n) {
    vector<int> v(n);
    iota(v.begin(), v.end(), 0);
    return v;
}

vector<int> randomCase(int n) {
    vector<int> v = bestCase(n);
    shuffle(v.begin(), v.end(), mt19937(42));
    return v;
}

// Undo a merge level by level: evens go left, odds go right, so every merge alternates between the two halves.
void spread(vector<int>& v) {
    if (v.size() < 2) return;
    vector<int> evens, odds;
    for (size_t i = 0; i < v.size(); i++) (i % 2 == 0 ? evens : odds).push_back(v[i]);
    spread(evens);
    spread(odds);
    copy(evens.begin(), evens.end(), v.begin());
    copy(odds.begin(), odds.end(), v.begin() + evens.size());
}

vector<int> worstCase(int n) {
    vector<int> v = bestCase(n);
    spread(v);
    return v;
}

struct Run {
    double ms;
    ll comparisons;
};

Run timeSort(const vector<int>& input, bool parallel) {
    Run best{1e18, 0};
    for (int round = 0; round < 3; round++) {
        vector<int> a = input, tmp(input.size());
        int n = (int)a.size();
        auto start = Clock::now();
        ll c = parallel ? parallelMergeSort(a, tmp, 0, n, THREAD_DEPTH) : mergeSort(a, tmp, 0, n);
        double ms = chrono::duration<double, milli>(Clock::now() - start).count();
        if (!is_sorted(a.begin(), a.end())) {
            cout << "ERROR: result is not sorted\n";
            exit(1);
        }
        if (ms < best.ms) best = {ms, c};
    }
    return best;
}

int main() {
    cout << "Hardware threads: " << thread::hardware_concurrency() << "\n";
    cout << "Worst-case array for n = 8: ";
    for (int x : worstCase(8)) cout << x << ' ';
    cout << "\n\n";

    cout << left << setw(9) << "case" << right << setw(10) << "n" << setw(14) << "comparisons"
         << setw(13) << "merge (ms)" << setw(15) << "parallel (ms)" << setw(10) << "speedup" << "\n";
    for (int n : {1 << 16, 1 << 18, 1 << 20, 1 << 22}) {
        for (string name : {"best", "random", "worst"}) {
            vector<int> data = name == "best" ? bestCase(n) : name == "random" ? randomCase(n) : worstCase(n);
            Run seq = timeSort(data, false);
            Run par = timeSort(data, true);
            cout << left << setw(9) << name << right << setw(10) << n << setw(14) << seq.comparisons
                 << fixed << setprecision(2) << setw(13) << seq.ms << setw(15) << par.ms
                 << setw(9) << seq.ms / par.ms << "x\n";
        }
        cout << "\n";
    }
}
