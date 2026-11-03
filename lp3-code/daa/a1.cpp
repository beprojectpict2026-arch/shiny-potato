/*
 * DAA Assignment 1 - Recursive and non-recursive (iterative) Fibonacci.
 *
 * Problem statement: Compute the n-th Fibonacci number using recursive
 * and iterative approaches and analyze time and space complexity.
 */
#include <iostream>
#include <ctime>
using namespace std;

long long calls = 0;

// Recursive Fibonacci: O(2^n) time, O(n) stack space
long long fibRecursive(int n) {
    calls++;
    if (n <= 1) return n;
    return fibRecursive(n - 1) + fibRecursive(n - 2);
}

// Iterative Fibonacci: O(n) time, O(1) space
long long fibIterative(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        long long next = a + b;
        a = b;
        b = next;
    }
    return a;
}

int main() {
    int n;
    cout << "Enter n: ";
    cin >> n;

    // --- Recursive ---
    calls = 0;
    clock_t startRec = clock();
    long long ansRec = fibRecursive(n);
    clock_t endRec = clock();
    double timeRec = (double)(endRec - startRec);

    // --- Iterative ---
    clock_t startIter = clock();
    long long ansIter = fibIterative(n);
    clock_t endIter = clock();
    double timeIter = (double)(endIter - startIter);

    cout << "\n--- Recursive ---\n";
    cout << "Fibonacci(" << n << ") = " << ansRec << "\n";
    cout << "Recursive calls: " << calls << "\n";
    cout << "Time taken: " << timeRec << " seconds\n";

    cout << "\n--- Iterative ---\n";
    cout << "Fibonacci(" << n << ") = " << ansIter << "\n";
    cout << "Time taken: " << timeIter << " seconds\n";

    return 0;
}
