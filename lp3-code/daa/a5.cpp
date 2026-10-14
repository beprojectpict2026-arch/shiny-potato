/*
 * DAA Assignment 5 - Analysis of Quick sort: deterministic vs randomized.
 *
 * Problem statement: implement Quick sort with a fixed pivot (last element, deterministic) and
 * with a pivot chosen uniformly at random, and compare them on random, sorted and reverse-sorted
 * inputs by counting comparisons and timing. Deterministic worst case is O(n^2) (sorted input);
 * the randomized version is O(n log n) in expectation on every input.
 * Libraries used (standard library only): <random> (seeded generator), <chrono>, <algorithm>.
 *
 * Driver: sorts arrays of 2000 elements of three kinds with both variants (fixed seed, so the
 * output is repeatable). No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 a5.cpp -o a5 && ./a5
 */
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>
using namespace std;

long long comparisons = 0;
mt19937 rng(1);

int partition(vector<int>& a, int lo, int hi) {
    int pivot = a[hi];                       // the pivot is the rightmost element
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        comparisons++;
        if (a[j] <= pivot) swap(a[++i], a[j]);
    }
    swap(a[i + 1], a[hi]);
    return i + 1;
}

void quickSort(vector<int>& a, int lo, int hi, bool randomized) {
    if (lo >= hi) return;
    if (randomized) {                        // move a random element into the pivot position
        int r = uniform_int_distribution<int>(lo, hi)(rng);
        swap(a[r], a[hi]);
    }
    int q = partition(a, lo, hi);
    quickSort(a, lo, q - 1, randomized);
    quickSort(a, q + 1, hi, randomized);
}

void run(const string& inputName, const vector<int>& data) {
    for (bool randomized : {false, true}) {
        vector<int> a = data;
        comparisons = 0;
        auto t0 = chrono::steady_clock::now();
        quickSort(a, 0, (int)a.size() - 1, randomized);
        double ms = chrono::duration<double, milli>(chrono::steady_clock::now() - t0).count();
        cout << left << setw(16) << inputName << setw(15) << (randomized ? "randomized" : "deterministic")
             << right << setw(12) << comparisons << setw(12) << fixed << setprecision(3) << ms
             << (is_sorted(a.begin(), a.end()) ? "" : "  NOT SORTED") << "\n";
    }
}

int main() {
    int n = 2000;
    vector<int> randomData(n), sortedData(n), reverseData(n);
    iota(randomData.begin(), randomData.end(), 0);
    shuffle(randomData.begin(), randomData.end(), rng);
    iota(sortedData.begin(), sortedData.end(), 0);
    for (int i = 0; i < n; i++) reverseData[i] = n - i;

    cout << "n = " << n << "   (n log2 n ~ 22000, n^2/2 ~ 2000000)\n";
    cout << left << setw(16) << "input" << setw(15) << "variant" << right << setw(12) << "comparisons"
         << setw(12) << "time (ms)" << "\n";
    run("random", randomData);
    run("already sorted", sortedData);
    run("reverse sorted", reverseData);
    cout << "\nConclusion: on sorted inputs the fixed pivot degrades to ~n^2/2 comparisons, while the\n"
            "random pivot stays near n log n for every input.\n";
    return 0;
}
