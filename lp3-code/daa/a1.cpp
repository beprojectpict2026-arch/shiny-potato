/*
 * DAA Assignment 1 - Recursive and non-recursive (iterative) Fibonacci.
 *
 * Problem statement: compute the n-th Fibonacci number with a recursive and an iterative
 * program and analyse time and space complexity (recursive: O(2^n) time, O(n) stack space;
 * iterative: O(n) time, O(1) extra space) by counting calls and measuring run time.
 * Libraries used (standard library only): <iostream>, <iomanip>, <chrono>.
 *
 * Driver: prints the first 10 numbers from both programs, then a table for n = 10..30.
 * No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 a1.cpp -o a1 && ./a1
 */
#include <chrono>
#include <iomanip>
#include <iostream>
using namespace std;

long long calls = 0;     // number of recursive calls made
int maxDepth = 0;        // deepest recursion level = stack space used

long long fibRecursive(int n, int depth = 1) {
    calls++;
    if (depth > maxDepth) maxDepth = depth;
    if (n <= 1) return n;
    return fibRecursive(n - 1, depth + 1) + fibRecursive(n - 2, depth + 1);
}

long long fibIterative(int n) {
    long long a = 0, b = 1;               // only the last two values are kept
    for (int i = 0; i < n; i++) {
        long long next = a + b;
        a = b;
        b = next;
    }
    return a;
}

int main() {
    cout << "First 10 numbers (recursive): ";
    for (int i = 0; i < 10; i++) cout << fibRecursive(i) << " ";
    cout << "\nFirst 10 numbers (iterative): ";
    for (int i = 0; i < 10; i++) cout << fibIterative(i) << " ";
    cout << "\n\n";

    cout << setw(3) << "n" << setw(9) << "F(n)" << setw(12) << "rec calls" << setw(8) << "depth"
         << setw(14) << "rec time(ms)" << setw(15) << "iter time(ms)" << "\n";
    for (int n = 10; n <= 30; n += 5) {
        calls = 0;
        maxDepth = 0;
        auto t0 = chrono::steady_clock::now();
        long long value = fibRecursive(n);
        auto t1 = chrono::steady_clock::now();
        long long check = fibIterative(n);
        auto t2 = chrono::steady_clock::now();
        double recMs = chrono::duration<double, milli>(t1 - t0).count();
        double iterMs = chrono::duration<double, milli>(t2 - t1).count();
        cout << setw(3) << n << setw(9) << value << setw(12) << calls << setw(8) << maxDepth
             << setw(14) << fixed << setprecision(4) << recMs << setw(15) << setprecision(6) << iterMs
             << (check == value ? "" : "  MISMATCH") << "\n";
    }
    cout << "\nConclusion: recursive calls grow ~1.6x per step of n (exponential) while the stack\n"
            "depth is only n; the iterative version does n additions with constant extra space.\n";
    return 0;
}
