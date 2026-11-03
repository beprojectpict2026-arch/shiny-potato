/*
 * DAA Assignment 5 - Deterministic vs Randomized Quick Sort
 *
 * Deterministic: Fixed pivot (e.g. last element). Worst case O(n^2) on sorted data.
 * Randomized: Random pivot chosen uniformly. Expected O(n log n) on all inputs.
 */
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

long long comparisons = 0;

int partition(vector<int>& a, int low, int high) {
    int pivot = a[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        comparisons++;
        if (a[j] <= pivot) {
            i++;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[high]);
    return i + 1;
}

void quickSort(vector<int>& a, int low, int high, bool isRandomized) {
    if (low >= high) return;

    if (isRandomized) {
        // Pick random pivot and swap with high
        int randomIdx = low + rand() % (high - low + 1);
        swap(a[randomIdx], a[high]);
    }

    int pi = partition(a, low, high);
    quickSort(a, low, pi - 1, isRandomized);
    quickSort(a, pi + 1, high, isRandomized);
}

void testSort(vector<int> a, bool isRandomized) {
    comparisons = 0;
    auto start = clock();
    quickSort(a, 0, a.size() - 1, isRandomized);
    auto end = clock();

    double timeTaken = (double)(end - start) * 1000.0 / CLOCKS_PER_SEC;

    if (isRandomized) cout << "Randomized QuickSort  : ";
    else              cout << "Deterministic QuickSort: ";
    
    for (int x: a) cout << x <<" "; 
    cout << "\nComparisons = " << comparisons << " | Time = " << timeTaken << " ms\n";
}

int main() {
    srand(time(0));
    int n;
    cout << "Enter number of elements: ";
    cin >> n;

    vector<int> arr(n);
    cout << "Enter " << n << " elements:\n";
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    cout << "\n--- Results ---\n";
    testSort(arr, false); // Deterministic
    testSort(arr, true);  // Randomized

    return 0;
}
