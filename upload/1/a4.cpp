/*
 * DAA Assignment 4 - N-Queens with the first queen already placed.
 * Using Hash Sets / Boolean lookup arrays for O(1) safety checks.
 *
 * Diagonals formula:
 * 1. Major diagonal (\): row - col + (n - 1)
 * 2. Minor diagonal (/): row + col
 */
#include <iostream>
#include <vector>
using namespace std;

int n;
vector<vector<int>> board;
vector<bool> cols;         // tracks occupied columns
vector<bool> diag1;        // tracks major diagonal (\) : row - col + (n - 1)
vector<bool> diag2;        // tracks minor diagonal (/) : row + col

void printBoard() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cout << (board[i][j] ? "Q " : ". ");
        }
        cout << "\n";
    }
}

bool solve(int row) {
    // Base Case: All queens are successfully placed
    if (row == n) return true;

    for (int col = 0; col < n; col++) {
        // O(1) check using lookup arrays
        if (!cols[col] && !diag1[row - col + n - 1] && !diag2[row + col]) {
            // Place Queen & mark sets
            board[row][col] = 1;
            cols[col] = true;
            diag1[row - col + n - 1] = true;
            diag2[row + col] = true;

            // Recurse to next row
            if (solve(row + 1)) return true;

            // Backtrack: Unmark
            board[row][col] = 0;
            cols[col] = false;
            diag1[row - col + n - 1] = false;
            diag2[row + col] = false;
        }
    }
    return false;
}

int main() {
    cout << "Enter board size (N): ";
    cin >> n;

    int firstCol;
    cout << "Enter column for 1st Queen in row 0 (0 to " << n - 1 << "): ";
    cin >> firstCol;

    // Initialize board and lookup sets
    board.assign(n, vector<int>(n, 0));
    cols.assign(n, false);
    diag1.assign(2 * n, false);
    diag2.assign(2 * n, false);

    // Place the 1st Queen manually in row 0
    board[0][firstCol] = 1;
    cols[firstCol] = true;
    diag1[0 - firstCol + n - 1] = true;
    diag2[0 + firstCol] = true;

    // Start solving from row 1 onwards
    if (solve(1)) {
        cout << "\nSolution:\n";
        printBoard();
    } else {
        cout << "\nNo solution exists with 1st Queen at row 0, column " << firstCol << ".\n";
    }

    return 0;
}
