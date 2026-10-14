/*
 * DAA Mini-project - Naive string matching vs Rabin-Karp.
 *
 * Problem statement: implement the naive string-matching algorithm (O(n*m) worst case) and the
 * Rabin-Karp algorithm (rolling hash, O(n+m) expected) and observe how they differ on the same
 * input: matches found, character comparisons, hash hits vs spurious hits, and run time.
 * Libraries used (standard library only): <string>, <vector>, <chrono>, <iostream>.
 *
 * Driver: a short text with a tiny modulus (forces hash collisions = spurious hits), then a
 * large worst-case text ("aaaa...ab") to compare run times. No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 mini_string_matching.cpp -o mini && ./mini
 */
#include <chrono>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Result {
    vector<int> matches;
    long long comparisons = 0;
    int spurious = 0;
};

// Slide the pattern over the text and compare character by character.
Result naive(const string& text, const string& pattern) {
    Result r;
    int n = text.size(), m = pattern.size();
    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        while (j < m) {
            r.comparisons++;
            if (text[i + j] != pattern[j]) break;
            j++;
        }
        if (j == m) r.matches.push_back(i);
    }
    return r;
}

// Compare rolling hashes first; compare characters only when the hashes are equal.
Result rabinKarp(const string& text, const string& pattern, long long mod) {
    Result r;
    const long long base = 256;
    int n = text.size(), m = pattern.size();
    long long high = 1;                      // base^(m-1) % mod: weight of the leading character
    for (int i = 1; i < m; i++) high = (high * base) % mod;
    long long pHash = 0, tHash = 0;
    for (int i = 0; i < m; i++) {
        pHash = (pHash * base + pattern[i]) % mod;
        tHash = (tHash * base + text[i]) % mod;
    }
    for (int i = 0; i + m <= n; i++) {
        if (pHash == tHash) {                // possible match: verify, it may be a collision
            r.comparisons += m;
            if (text.compare(i, m, pattern) == 0) r.matches.push_back(i);
            else r.spurious++;
        }
        if (i + m < n)                       // roll the hash to the next window in O(1)
            tHash = ((tHash - text[i] * high % mod + mod) * base + text[i + m]) % mod;
    }
    return r;
}

void print(const string& name, const Result& r, double ms) {
    cout << left << setw(12) << name << right << setw(9) << r.matches.size() << setw(13) << r.comparisons
         << setw(10) << r.spurious << setw(12) << fixed << setprecision(3) << ms << "\n";
}

int main() {
    string text = "ABABDABACDABABCABABABABCABAB", pattern = "ABABC";
    cout << "Text    : " << text << "\nPattern : " << pattern << "\n";
    Result a = naive(text, pattern);
    Result b = rabinKarp(text, pattern, 7);  // tiny modulus -> many collisions
    auto show = [](const Result& r) {
        for (int p : r.matches) cout << p << " ";
    };
    cout << "Naive      : matches at "; show(a); cout << "-> " << a.comparisons << " character comparisons\n";
    cout << "Rabin-Karp : matches at "; show(b); cout << "-> " << b.comparisons << " character comparisons, "
         << b.spurious << " spurious hash hits (mod = 7)\n";
    cout << "Same matches: " << (a.matches == b.matches ? "true" : "false") << "\n";

    string bigText = string(20000, 'a') + "b", bigPattern = string(200, 'a') + "b";
    auto t0 = chrono::steady_clock::now();
    Result na = naive(bigText, bigPattern);
    auto t1 = chrono::steady_clock::now();
    Result rk = rabinKarp(bigText, bigPattern, 1000003);
    auto t2 = chrono::steady_clock::now();
    cout << "\nLarge worst-case input (text " << bigText.size() << " chars, pattern " << bigPattern.size() << " chars):\n";
    cout << left << setw(12) << "algorithm" << right << setw(9) << "matches" << setw(13) << "comparisons"
         << setw(10) << "spurious" << setw(12) << "time (ms)" << "\n";
    print("naive", na, chrono::duration<double, milli>(t1 - t0).count());
    print("rabin-karp", rk, chrono::duration<double, milli>(t2 - t1).count());
    return 0;
}
