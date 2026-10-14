/*
 * DAA Assignment 3 - 0-1 Knapsack using dynamic programming.
 *
 * Problem statement: given n items with weights and values and a knapsack of capacity W, pick a
 * subset (each item whole or not at all) with maximum total value. Bottom-up table
 * T(i,j) = max(T(i-1,j), value_i + T(i-1, j-weight_i)); time and space O(n*W); the chosen items
 * are recovered by tracing the table backwards.
 * Libraries used (standard library only): <iostream>, <iomanip>, <vector>, <algorithm>.
 *
 * Driver: the manual's example (weights 2,3,4,5; values 3,4,5,6; capacity 5). No input is taken
 * at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 a3.cpp -o a3 && ./a3
 */
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> names = {"Mirror", "Silver nugget", "Painting", "Vase"};
    vector<int> weight = {2, 3, 4, 5};
    vector<int> value = {3, 4, 5, 6};
    int n = names.size(), capacity = 5;

    // table[i][j] = best value using the first i items with capacity j (row 0 / column 0 stay 0)
    vector<vector<int>> table(n + 1, vector<int>(capacity + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= capacity; j++) {
            table[i][j] = table[i - 1][j];                       // skip item i
            if (weight[i - 1] <= j)                              // or take it, if it fits
                table[i][j] = max(table[i][j], value[i - 1] + table[i - 1][j - weight[i - 1]]);
        }
    }

    cout << "Capacity = " << capacity << " kg\nDP table T(i, j): rows = items 0..n, columns = capacity 0..W\n";
    cout << setw(8) << "";
    for (int j = 0; j <= capacity; j++) cout << setw(4) << j;
    cout << "\n";
    for (int i = 0; i <= n; i++) {
        cout << setw(8) << (i == 0 ? string("none") : "item " + to_string(i));
        for (int j = 0; j <= capacity; j++) cout << setw(4) << table[i][j];
        cout << "\n";
    }

    // trace back from the last cell: if the value changed from the row above, item i was taken
    vector<int> chosen;
    int j = capacity;
    for (int i = n; i >= 1; i--) {
        if (table[i][j] != table[i - 1][j]) {
            chosen.push_back(i);
            j -= weight[i - 1];
        }
    }
    reverse(chosen.begin(), chosen.end());

    int totalWeight = 0;
    cout << "\nMaximum value = " << table[n][capacity] << "\nItems taken:\n";
    for (int i : chosen) {
        cout << "  " << names[i - 1] << " (weight " << weight[i - 1] << ", value " << value[i - 1] << ")\n";
        totalWeight += weight[i - 1];
    }
    cout << "Total weight = " << totalWeight << "\n";
    return 0;
}
