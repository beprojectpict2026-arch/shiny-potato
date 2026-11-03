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

#include <iostream>
#include <algorithm>
using namespace std;

// Function to calculate maximum profit
int knapsack(int n, int W, int wt[], int val[])
{
    int dp[101][101] = {0};

    for(int i = 1; i <= n; i++)
    {
        for(int j = 1; j <= W; j++)
        {
            if(wt[i-1] <= j)
                dp[i][j] = max(dp[i-1][j],
                    val[i-1] + dp[i-1][j-wt[i-1]]);
            else
                dp[i][j] = dp[i-1][j];
        }
    }

    return dp[n][W];
}

int main()
{
    int n, W;
    int wt[100], val[100];

    cout << "Enter number of items: ";
    cin >> n;

    cout << "Enter weights:\n";
    for(int i = 0; i < n; i++)
        cin >> wt[i];

    cout << "Enter values:\n";
    for(int i = 0; i < n; i++)
        cin >> val[i];

    cout << "Enter capacity: ";
    cin >> W;

    cout << "Maximum Profit = "
         << knapsack(n, W, wt, val);

    return 0;
}
