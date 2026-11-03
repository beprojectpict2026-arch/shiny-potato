/*
 * DAA Assignment 2 - Huffman Encoding (Greedy Approach)
 *
 * Concepts:
 * 1. Greedy choice: Repeatedly pick 2 nodes with lowest frequency using Min-Heap.
 * 2. Tree creation: Merge them into a parent node with sum of their frequencies.
 * 3. Assign codes: Left edge = '0', Right edge = '1'.
 *
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)

 ```
Enter number of characters: 4

Enter character and frequency:
A 1
B 2
C 3
D 4
```
 */


#include <iostream>
#include <queue>
#include<vector>
using namespace std;

struct Node {
    char ch;
    int freq;
    Node *left, *right;

    Node(char c, int f) {
        ch = c;
        freq = f;
        left = right = NULL;
    }
};

// Min Heap
struct Compare {
    bool operator()(Node* a, Node* b) {
        return a->freq > b->freq;
    }
};

// Print Huffman Codes
void printCodes(Node* root, string code) {
    if (root == NULL)
        return;

    if (root->left == NULL && root->right == NULL) {
        cout << root->ch << " : " << code << endl;
        return;
    }

    printCodes(root->left, code + "0");
    printCodes(root->right, code + "1");
}

void printTree(Node* root, int space = 0) {
    if (root == NULL)
        return;

    space += 5;

    // Print right subtree
    printTree(root->right, space);

    // Print current node
    cout << endl;
    for (int i = 5; i < space; i++)
        cout << " ";

    cout << root->ch << "(" << root->freq << ")";

    // Print left subtree
    printTree(root->left, space);
}

int main() {
    int n;
    cout << "Enter number of characters: ";
    cin >> n;

    priority_queue<Node*, vector<Node*>, Compare> pq;
    char ch;
    int freq;
    
    cout << "Enter character and frequency:\n";
    for (int i = 0; i < n; i++) {
        cin >> ch >> freq;
        pq.push(new Node(ch, freq));
    }

    while (pq.size() > 1) {
        Node* left = pq.top();
        pq.pop();
        Node* right = pq.top();
        pq.pop();
        Node* parent = new Node('$', left->freq + right->freq);
        parent->left = left;
        parent->right = right;
        pq.push(parent);
    }

    cout << "\nHuffman Codes:\n";
    printCodes(pq.top(), "");
    return 0;
}
