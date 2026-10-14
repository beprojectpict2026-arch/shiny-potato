/*
 * DAA Assignment 4 - N-Queens with the first queen already placed (backtracking).
 *
 * Problem statement: on an N x N board the first queen is fixed in row 0 at a given column;
 * place the remaining N-1 queens row by row using backtracking (try a safe column, recurse,
 * undo the choice on failure) so no two queens attack each other, then print the final board.
 * Libraries used (standard library only): <iostream>, <vector>.
 *
 * Driver: N=8 with the first queen in column 3, N=6 with column 1, and N=4 with column 0
 * (which has no solution). No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 a4.cpp -o a4 && ./a4
 */
#include <cstdlib>
#include <iostream>
#include <vector>
using namespace std;

// board[r] = column of the queen in row r (-1 = empty)
bool isSafe(const vector<int>& board, int row, int col) {
    for (int r = 0; r < row; r++) {
        // same column, or same diagonal (row distance equals column distance)
        if (board[r] == col || abs(board[r] - col) == row - r) return false;
    }
    return true;
}

bool place(vector<int>& board, int row, int n) {
    if (row == n) return true;               // all queens placed
    for (int col = 0; col < n; col++) {
        if (isSafe(board, row, col)) {
            board[row] = col;
            if (place(board, row + 1, n)) return true;
            board[row] = -1;                 // backtrack: undo and try the next column
        }
    }
    return false;
}

int main() {
    int tests[3][2] = {{8, 3}, {6, 1}, {4, 0}};  // {N, column of the first queen}
    for (auto& t : tests) {
        int n = t[0], firstCol = t[1];
        cout << "N = " << n << ", first queen at row 0, column " << firstCol << ":\n";
        vector<int> board(n, -1);
        board[0] = firstCol;                 // the first queen is given
        if (place(board, 1, n)) {
            for (int r = 0; r < n; r++) {
                cout << "  ";
                for (int c = 0; c < n; c++) cout << (board[r] == c ? "Q " : ". ");
                cout << "\n";
            }
            cout << "  queen columns per row:";
            for (int c : board) cout << " " << c;
            cout << "\n";
        } else {
            cout << "  no solution exists with the first queen there\n";
        }
        cout << "\n";
    }
    return 0;
}
