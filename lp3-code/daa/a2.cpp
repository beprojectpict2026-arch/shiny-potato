/*
 * DAA Assignment 2 - Huffman encoding using a greedy strategy.
 *
 * Problem statement: build a Huffman tree by repeatedly merging the two least frequent nodes
 * (greedy choice, using a min-heap), derive the prefix codes, then encode and decode text.
 * Time complexity O(n log n) for n distinct characters.
 * Libraries used (standard library only): <queue> (priority_queue as min-heap), <map>, <vector>.
 *
 * Driver: (1) the manual's example a:5 b:9 c:12 d:13 e:16 f:45, (2) the text "huffman coding".
 * No input is taken at runtime.
 *
 * Compile and run:  g++ -std=c++17 -O2 a2.cpp -o a2 && ./a2
 */
#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <vector>
using namespace std;

struct Node {
    int freq;
    char symbol;    // meaningful only for leaves
    int left, right;  // indices into the node pool, -1 for a leaf
};

vector<Node> pool;  // all tree nodes live here; children are referred to by index

// Greedy step: take the two smallest nodes, merge them, push the parent back.
int buildTree(const map<char, int>& freqs) {
    // min-heap of (frequency, node index); the index breaks ties the same way every run
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> heap;
    pool.clear();
    for (auto& [symbol, f] : freqs) {
        pool.push_back({f, symbol, -1, -1});
        heap.push({f, (int)pool.size() - 1});
    }
    while (heap.size() > 1) {
        int a = heap.top().second; heap.pop();
        int b = heap.top().second; heap.pop();
        pool.push_back({pool[a].freq + pool[b].freq, '#', a, b});
        heap.push({pool.back().freq, (int)pool.size() - 1});
    }
    return heap.top().second;  // root
}

// Left edge = 0, right edge = 1; the path to a leaf is its code.
void makeCodes(int node, const string& prefix, map<char, string>& codes) {
    if (pool[node].left == -1) {
        codes[pool[node].symbol] = prefix.empty() ? "0" : prefix;
        return;
    }
    makeCodes(pool[node].left, prefix + "0", codes);
    makeCodes(pool[node].right, prefix + "1", codes);
}

string encode(const string& text, const map<char, string>& codes) {
    string bits;
    for (char c : text) bits += codes.at(c);
    return bits;
}

string decode(const string& bits, int root) {
    string out;
    int node = root;
    for (char bit : bits) {
        node = (bit == '0') ? pool[node].left : pool[node].right;
        if (pool[node].left == -1) {  // reached a leaf
            out += pool[node].symbol;
            node = root;
        }
    }
    return out;
}

int main() {
    map<char, int> freqs = {{'a', 5}, {'b', 9}, {'c', 12}, {'d', 13}, {'e', 16}, {'f', 45}};
    int root = buildTree(freqs);
    map<char, string> codes;
    makeCodes(root, "", codes);
    cout << "Example from the manual:\n";
    int totalBits = 0, totalFreq = 0;
    for (auto& [symbol, f] : freqs) {
        cout << "  " << symbol << ": freq=" << f << "  code=" << codes[symbol] << "\n";
        totalBits += f * (int)codes[symbol].size();
        totalFreq += f;
    }
    cout << "  total bits: " << totalBits << " vs fixed 3-bit: " << 3 * totalFreq << "\n";

    string text = "huffman coding";
    map<char, int> textFreqs;
    for (char c : text) textFreqs[c]++;
    root = buildTree(textFreqs);
    codes.clear();
    makeCodes(root, "", codes);
    string bits = encode(text, codes);
    cout << "\nText '" << text << "': " << text.size() * 8 << " bits as ASCII -> " << bits.size()
         << " bits with Huffman\n  encoded: " << bits << "\n  decoded: " << decode(bits, root)
         << "\n  round trip OK: " << (decode(bits, root) == text ? "true" : "false") << "\n";
    return 0;
}
