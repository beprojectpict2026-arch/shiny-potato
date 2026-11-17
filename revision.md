# CSDF & Information Retrieval (IR) — Viva Preparation

**Class:** 302 / 303  
**Purpose:** Frequently asked LP4 viva questions  
**Order:** Higher-frequency topics first. Mini-project questions are excluded.

---

# Part 1: Information Retrieval (IR)

## 1. Explain XML Parsing and Web Graph Generation.

**XML parsing** is the process of reading an XML document and extracting meaningful information from its structured tags and attributes.

In our assignment, XML parsing is used to extract web pages and their hyperlinks and represent them as a directed graph.

**Steps:**
1. Read the XML file.
2. Parse it using Python's XML parser.
3. Extract page identifiers or URLs.
4. Extract hyperlinks between pages.
5. Represent each page as a node.
6. Represent each hyperlink as a directed edge.
7. Apply PageRank to calculate page importance.

**Example:**

Suppose page A links to B and C, and B links to C.

The graph contains:
- A → B
- A → C
- B → C

**Which XML parser can be used?**

Python provides the `xml.etree.ElementTree` module for parsing XML documents.

```python
import xml.etree.ElementTree as ET

tree = ET.parse("data.xml")
root = tree.getroot()

for element in root:
    print(element.tag, element.attrib)
```

**What is the difference between XML and HTML?**

- XML is used to store and transport structured data.
- HTML is used to structure and display content on web pages.
- XML allows custom tags, whereas HTML uses predefined tags.

---

## 2. Explain the PageRank Algorithm.

PageRank is an algorithm developed by Google to measure the importance of web pages based on the links pointing to them.

**Basic idea:** A page is considered important if many pages link to it, especially if those pages are themselves important.

**PageRank formula:**

\[
PR(A)=\frac{1-d}{N}
+d\sum_{T_i\in In(A)}
\frac{PR(T_i)}{C(T_i)}
\]

Where:

- \(PR(A)\): PageRank of page A.
- \(d\): Damping factor, generally 0.85.
- \(N\): Total number of pages.
- \(In(A)\): Pages linking to A.
- \(PR(T_i)\): PageRank of the linking page.
- \(C(T_i)\): Number of outgoing links from page \(T_i\).

**What is the damping factor?**

The damping factor represents the probability that a user continues clicking links rather than jumping to a random page.

A commonly used value is 0.85.

**How is page importance decided?**

Page importance depends on:
1. Number of incoming links.
2. Importance of pages providing those links.
3. Number of outgoing links from those pages.

A link from an important page generally contributes more than a link from a less important page.

**What is the difference between a web crawler and PageRank?**

| Web Crawler | PageRank |
|---|---|
| Discovers web pages. | Calculates page importance. |
| Visits URLs and follows links. | Analyses the link structure. |
| Collects web content. | Produces ranking scores. |

**What is a dangling node?**

A dangling node is a web page that has no outgoing links. It can cause problems during PageRank calculation, so its rank must be redistributed appropriately.

**What is topic-specific PageRank?**

Topic-specific PageRank gives higher importance to pages relevant to a particular topic.

Unlike normal PageRank, which distributes random jumps across all pages, topic-specific PageRank uses a preference vector that favours selected topic-related pages.

---

## 3. What is TF-IDF?

TF-IDF stands for **Term Frequency–Inverse Document Frequency**.

It is a statistical technique used in Information Retrieval to measure how important a word is in a document relative to a collection of documents.

It gives higher importance to words that occur frequently in a particular document but are uncommon across the entire document collection.

### A. Term Frequency (TF)

TF measures how frequently a term occurs in a document.

\[
TF(t,d)=\frac{f_{t,d}}{\text{Total number of terms in }d}
\]

Where:
- \(f_{t,d}\): Frequency of term \(t\) in document \(d\).

### B. Inverse Document Frequency (IDF)

IDF measures how rare or common a term is across all documents.

\[
IDF(t)=\log\left(\frac{N}{DF(t)}\right)
\]

Where:
- \(N\): Total number of documents.
- \(DF(t)\): Number of documents containing term \(t\).

### C. TF-IDF Formula

\[
\boxed{TFIDF(t,d)=TF(t,d)\times IDF(t)}
\]

**Example:**

If a word occurs frequently in one document but rarely in other documents, it receives a high TF-IDF score.

Words like "the", "is" and "and" usually receive low importance because they appear in many documents.

**Applications:**
- Search engines.
- Document similarity.
- Information retrieval.
- Text classification.
- Keyword extraction.

---

## 4. What is a Web Crawler?

A web crawler is an automated program that visits web pages, downloads their content and discovers other pages by following hyperlinks.

It is also called a spider or bot.

**Working:**
1. Start with a list of URLs called seed URLs.
2. Visit a URL and download its page.
3. Extract useful information and hyperlinks.
4. Add new URLs to a queue.
5. Visit the newly discovered URLs.
6. Repeat until the crawling condition is satisfied.

**What is Scrapy?**

Scrapy is a Python framework used to build web crawlers and extract data from websites.

Important components:

- **Spider:** Defines what websites to crawl and how to extract data.
- **Scheduler:** Maintains requests waiting to be processed.
- **Downloader:** Downloads web pages.
- **Response:** Contains the downloaded page.
- **Parser:** Extracts information from the response.
- **Item Pipeline:** Processes and stores extracted data.

**Difference between `get()` and `getall()` in Scrapy:**

- `get()` returns the first matching value.
- `getall()` returns all matching values as a list.

**What is robots.txt?**

It is a file that specifies which parts of a website automated crawlers are allowed or disallowed to access.

---

## 5. What is Cosine Similarity?

Cosine similarity measures the similarity between two vectors by calculating the cosine of the angle between them.

It is commonly used to measure similarity between text documents represented as TF-IDF vectors.

**Formula:**

\[
\boxed{
\text{Cosine Similarity}(A,B)=
\frac{A\cdot B}{\|A\|\|B\|}
}
\]

Expanded formula:

\[
\text{Cosine Similarity}(A,B)=
\frac{\sum_{i=1}^{n} A_iB_i}
{\sqrt{\sum_{i=1}^{n}A_i^2}
\sqrt{\sum_{i=1}^{n}B_i^2}}
\]

**Example:**

Let:

\[
A=(1,1,0)
\]

\[
B=(1,0,1)
\]

Dot product:

\[
A\cdot B=(1\times1)+(1\times0)+(0\times1)=1
\]

Magnitude of A:

\[
\|A\|=\sqrt{1^2+1^2+0^2}=\sqrt{2}
\]

Magnitude of B:

\[
\|B\|=\sqrt{1^2+0^2+1^2}=\sqrt{2}
\]

Therefore:

\[
\text{Similarity}=\frac{1}{\sqrt{2}\times\sqrt{2}}
\]

\[
\boxed{\text{Similarity}=0.5}
\]

**Interpretation:**
- 1: Completely similar vectors.
- 0: No similarity in the direction of the vectors.
- -1: Completely opposite vectors, possible in representations containing negative values.

For ordinary non-negative TF-IDF vectors, cosine similarity generally ranges from 0 to 1.

**Why use cosine similarity instead of Euclidean distance?**

Cosine similarity focuses on the angle between vectors rather than their absolute magnitude. It is useful when document lengths differ.

---

## 6. What is MapReduce?

MapReduce is a programming model used to process large datasets in a distributed manner across multiple machines.

It has three main stages:

### A. Map
The mapper processes input data and generates key-value pairs.

Example: For input `Apple Ball Apple`

```text
(Apple, 1)
(Ball, 1)
(Apple, 1)
```

### B. Shuffle and Sort
Groups all values having the same key.

```text
(Apple, [1, 1])
(Ball, [1])
```

### C. Reduce
Combines the grouped values to generate the final output.

```text
(Apple, 2)
(Ball, 1)
```

**What is the use of MapReduce?**

- Large-scale data processing.
- Distributed computation.
- Word counting.
- Log analysis.
- Data aggregation.

**What is Hadoop?**

Hadoop is an open-source framework used for distributed storage and processing of large datasets.

**What is HDFS?**

HDFS stands for Hadoop Distributed File System. It stores large files across multiple machines by splitting them into blocks and replicating them.

---

## 7. What is Text Preprocessing? Explain its Steps.

Text preprocessing is the process of cleaning and transforming raw text into a structured format suitable for analysis.

**Steps:**

1. **Lowercasing:** Convert all text into lowercase.
2. **Tokenization:** Split text into individual words or sentences.
3. **Removing punctuation:** Remove unnecessary punctuation marks.
4. **Removing stop words:** Remove common words such as "is", "the", "and".
5. **Stemming:** Reduce words to their root-like form.
6. **Lemmatization:** Convert words into their meaningful dictionary base form.
7. **Normalization:** Standardize text into a consistent format.

**Why is preprocessing needed?**

- Removes unnecessary information.
- Reduces vocabulary size.
- Improves processing efficiency.
- Helps algorithms identify meaningful patterns.
- Improves the quality of text analysis.

**What is the difference between stemming and lemmatization?**

| Stemming | Lemmatization |
|---|---|
| Removes prefixes or suffixes using rules. | Converts words into dictionary base forms. |
| May produce invalid words. | Produces meaningful words. |
| Generally faster. | Usually more computationally intensive. |
| Example: Studies → Studi | Example: Studies → Study |

**What are stop words?**

Stop words are common words that generally carry little useful information for a particular text-processing task.

Examples: is, the, a, an, and, of.

---

## 8. What is the Jaccard Coefficient?

The Jaccard coefficient measures similarity between two sets by calculating the ratio of their intersection to their union.

**Formula:**

\[
\boxed{
J(A,B)=\frac{|A\cap B|}{|A\cup B|}
}
\]

Where:
- \(A\cap B\): Common elements.
- \(A\cup B\): All unique elements from both sets.

**Example:**

Let:

\[
A=\{apple, banana, mango\}
\]

\[
B=\{banana, mango, orange\}
\]

Intersection:

\[
A\cap B=\{banana,mango\}
\]

Union:

\[
A\cup B=\{apple,banana,mango,orange\}
\]

Therefore:

\[
J(A,B)=\frac{2}{4}=\boxed{0.5}
\]

**Difference between Jaccard and Cosine Similarity:**

- Jaccard measures overlap between sets.
- Cosine similarity measures the angle between vectors.
- Jaccard is commonly used for set similarity.
- Cosine similarity is commonly used for document vectors.

---

## 9. What are Evaluation Metrics in Information Retrieval?

Evaluation metrics measure how effectively an information retrieval system retrieves relevant documents.

### A. Precision

Precision measures how many retrieved documents are actually relevant.

\[
\boxed{
Precision=\frac{TP}{TP+FP}
}
\]

### B. Recall

Recall measures how many relevant documents were successfully retrieved.

\[
\boxed{
Recall=\frac{TP}{TP+FN}
}
\]

### C. F1 Score

F1 score is the harmonic mean of precision and recall.

\[
\boxed{
F1=2\times\frac{Precision\times Recall}{Precision+Recall}
}
\]

Where:
- TP: True Positives.
- FP: False Positives.
- FN: False Negatives.

**Example:**

Suppose:
- 10 documents are retrieved.
- 8 retrieved documents are relevant.
- Total relevant documents are 20.

Then:

\[
Precision=\frac{8}{10}=0.8
\]

\[
Recall=\frac{8}{20}=0.4
\]

\[
F1=2\times\frac{0.8\times0.4}{0.8+0.4}
\]

\[
\boxed{F1=0.5333}
\]

**Difference between precision and recall:**

- Precision focuses on correctness of retrieved results.
- Recall focuses on completeness of retrieved results.

---

## 10. What is Extractive and Abstractive Summarization?

**Extractive summarization:**

It selects important sentences directly from the original document and combines them to create a shorter summary.

**Abstractive summarization:**

It understands the main meaning of the document and generates new sentences to express the important information.

| Extractive | Abstractive |
|---|---|
| Selects existing sentences. | Generates new sentences. |
| Uses original wording. | Can use different wording. |
| Generally simpler. | Generally more complex. |
| Example: TextRank. | Example: Transformer-based language models. |

---

## 11. What is NLP? Give Real-Life Applications.

NLP stands for **Natural Language Processing**.

It is a branch of Artificial Intelligence that enables computers to understand, process and generate human language.

**Applications:**
1. Chatbots and virtual assistants.
2. Machine translation.
3. Sentiment analysis.
4. Spam email detection.
5. Speech recognition.
6. Text summarization.
7. Search engines.
8. Grammar correction.

---

## 12. What is Normalization in Information Retrieval?

Normalization is the process of converting text into a consistent format before processing.

Examples:
- Converting text to lowercase.
- Removing unnecessary punctuation.
- Standardizing dates or numbers.
- Handling variations in word forms.

It helps reduce differences in text that do not affect its intended meaning.

---

# Part 2: Cyber Security and Digital Forensics (CSDF)

## 13. Explain Log Capturing, Log Ingestion and Event Correlation.

### What is a log?

A log is a record of events or activities generated by a computer system, application or network device.

Examples:
- User login attempts.
- File access.
- System errors.
- Network connections.
- Application failures.

### What is log capturing?

Log capturing is the process of collecting logs from different sources such as servers, applications, operating systems and network devices.

### What is log ingestion?

Log ingestion is the process of collecting logs and importing them into a centralized system for storage, processing and analysis.

### What is event correlation?

Event correlation is the process of analysing multiple related events to identify patterns, suspicious activities or security incidents.

**Example:**

Suppose a user enters an incorrect password 20 times within one minute.

- Each failed login is recorded as a log.
- Logs are collected by the monitoring system.
- Event correlation identifies repeated failures from the same IP address.
- The system can flag the activity as a possible brute-force attack.

**Steps involved:**

1. Log collection.
2. Log ingestion.
3. Log parsing and normalization.
4. Event correlation.
5. Alert generation.
6. Investigation and response.

**What is SIEM?**

SIEM stands for Security Information and Event Management.

It collects and analyses security logs from different sources to detect threats and generate alerts.

Examples: Splunk, IBM QRadar and Microsoft Sentinel.

**Difference between log capturing and event correlation:**

- Log capturing collects event records.
- Event correlation analyses multiple records to identify meaningful patterns.

---

## 14. Explain Hashing and Hashing Algorithms.

Hashing is the process of converting input data of arbitrary length into a fixed-length output called a hash or message digest.

**Properties of a cryptographic hash function:**

1. Deterministic: Same input always produces the same hash.
2. Fixed-length output.
3. One-way: Computationally infeasible to reverse.
4. Avalanche effect: Small input changes produce significantly different hashes.
5. Collision resistance: Difficult to find two different inputs with the same hash.

**Applications:**
- Password storage.
- Digital signatures.
- File integrity verification.
- Digital forensics.
- Blockchain.

**What is a collision?**

A collision occurs when two different input values produce the same hash output.

\[
H(A)=H(B),\quad A\neq B
\]

A secure hash algorithm should make finding such collisions computationally infeasible.

---

## 15. Explain SHA-256.

SHA-256 stands for **Secure Hash Algorithm 256-bit**.

It is a cryptographic hash function belonging to the SHA-2 family.

It converts input data of any size into a fixed 256-bit hash value.

**Important properties:**

- Output size: 256 bits.
- Output size: 32 bytes.
- Hexadecimal representation: 64 characters.
- One-way function.
- Designed to be collision-resistant.

**Why is it called SHA-256?**

Because its output digest is 256 bits long.

\[
256\text{ bits}=\frac{256}{8}=32\text{ bytes}
\]

Each hexadecimal character represents 4 bits.

\[
\frac{256}{4}=64\text{ hexadecimal characters}
\]

**What is the significance of 256?**

It represents the output length of the hash in bits. The theoretical output space contains:

\[
2^{256}
\]

possible hash values.

**How many permutations are possible in SHA-256?**

The SHA-256 output space contains \(2^{256}\) possible values. This is the number of possible output values, not the number of permutations performed internally by the algorithm.

**What is the difference between SHA-1 and SHA-2?**

| SHA-1 | SHA-2 |
|---|---|
| Produces a 160-bit hash. | Includes 224, 256, 384 and 512-bit variants. |
| Considered insecure against collision attacks. | SHA-256 and SHA-512 remain widely used secure hash functions. |
| Older algorithm. | Newer family of algorithms. |

**How is SHA-256 used in digital forensics?**

It generates a hash of a digital evidence file. The hash can be calculated before and after forensic analysis to check whether the evidence has changed.

Example in Python:

```python
import hashlib

with open("evidence.jpg", "rb") as file:
    data = file.read()

hash_value = hashlib.sha256(data).hexdigest()

print(hash_value)
```

---

## 16. Explain Email Header Analysis.

Email header analysis is the process of examining email metadata to identify the sender, receiver, route and authenticity of an email.

**Important email header fields:**

| Header | Meaning |
|---|---|
| From | Sender's displayed email address. |
| To | Recipient's email address. |
| Subject | Email subject. |
| Date | Date and time of sending. |
| Received | Servers through which the email passed. |
| Return-Path | Address used for handling delivery failures. |
| Message-ID | Unique identifier of the email. |
| Reply-To | Address to which replies should be sent. |

**How can we trace an email?**

1. Obtain the original email with full headers.
2. Examine the Received fields.
3. Read Received headers from bottom to top to understand the route chronologically.
4. Identify originating and intermediate mail servers.
5. Check sender-related information.
6. Verify SPF, DKIM and DMARC results.
7. Look for suspicious or inconsistent details.

**What is email spoofing?**

Email spoofing is an attack in which an attacker forges the sender address to make an email appear to originate from a trusted source.

---

## 17. What are SPF, DKIM and DMARC?

These are email authentication mechanisms used to reduce email spoofing and phishing.

**SPF — Sender Policy Framework**

It specifies which mail servers are authorized to send emails on behalf of a domain.

**DKIM — DomainKeys Identified Mail**

It adds a digital signature to an email. The receiver verifies the signature using the sender domain's public key.

**DMARC — Domain-based Message Authentication, Reporting and Conformance**

It tells receiving mail servers how to handle emails that fail authentication checks and provides reporting mechanisms.

**Difference:**

| SPF | DKIM | DMARC |
|---|---|---|
| Checks authorized sending servers. | Verifies the email's digital signature. | Defines handling policies and reporting. |
| Uses DNS records. | Uses public-key cryptography. | Uses domain policy and alignment checks. |

---

## 18. What is the CIA Triad?

CIA stands for **Confidentiality, Integrity and Availability**.

It represents the three fundamental principles of information security.

### A. Confidentiality

Ensures that information is accessible only to authorized users.

Example: Passwords and encryption.

### B. Integrity

Ensures that information is accurate and has not been modified without authorization.

Example: Hashing and digital signatures.

### C. Availability

Ensures that systems and data are available whenever authorized users need them.

Example: Backups, redundancy and disaster recovery.

---

## 19. What are the Different Types of Cyber Attacks?

Common cyber attacks include:

1. **Phishing:** Tricking users into revealing sensitive information through fake emails or websites.
2. **Malware:** Malicious software designed to damage or gain unauthorized access to systems.
3. **Ransomware:** Malware that encrypts files and demands payment.
4. **Brute-force attack:** Repeatedly trying different passwords to gain access.
5. **SQL Injection:** Injecting malicious SQL statements into application inputs.
6. **Denial of Service (DoS):** Making a service unavailable by overwhelming it with requests.
7. **Man-in-the-Middle (MITM):** Intercepting communication between two parties.
8. **Cross-Site Scripting (XSS):** Injecting malicious scripts into web pages viewed by other users.

---

## 20. What is SQL Injection?

SQL Injection is a web security vulnerability in which an attacker inserts malicious SQL statements into application inputs to manipulate database queries.

**Example:**

Suppose an application constructs a query like:

```sql
SELECT * FROM users
WHERE username = 'input'
AND password = 'input';
```

If user input is directly concatenated into the query, an attacker may manipulate the SQL condition to bypass authentication.

**Prevention:**

1. Use parameterized queries.
2. Validate user input.
3. Avoid constructing SQL queries using string concatenation.
4. Apply least-privilege database permissions.
5. Use secure coding practices.

---

## 21. What is Normalization?

Normalization is the process of organizing data to reduce redundancy and improve consistency.

In database systems, normalization involves dividing data into related tables and defining relationships between them.

**Common normal forms:**

- **1NF:** Each column contains atomic values, with no repeating groups.
- **2NF:** Must be in 1NF and have no partial dependency on a candidate key.
- **3NF:** Must be in 2NF and have no transitive dependency of non-key attributes on a candidate key.

**Benefits:**
- Reduces data duplication.
- Improves data consistency.
- Simplifies database maintenance.
- Prevents update, insertion and deletion anomalies.

---

## 22. What is Overfitting and Underfitting?

These are two problems encountered while training machine learning models.

**Overfitting:**

A model learns the training data too closely, including noise and unnecessary details.

- High training accuracy.
- Poor performance on unseen data.
- Model has poor generalization.

**Underfitting:**

A model is too simple to learn the underlying patterns in the data.

- Poor training accuracy.
- Poor testing accuracy.
- Model fails to capture important relationships.

| Overfitting | Underfitting |
|---|---|
| Model is too complex. | Model is too simple. |
| Memorizes training data. | Fails to learn patterns. |
| High variance. | High bias. |

**How can overfitting be reduced?**

- Regularization.
- Cross-validation.
- More training data.
- Dropout.
- Reducing model complexity.

**How can underfitting be reduced?**

- Increase model complexity.
- Add useful features.
- Train for more iterations.
- Reduce excessive regularization.

---

# Part 3: Quick Revision

| Question | Short Answer |
|---|---|
| TF-IDF full form | Term Frequency–Inverse Document Frequency |
| NLP full form | Natural Language Processing |
| XML full form | Extensible Markup Language |
| HDFS full form | Hadoop Distributed File System |
| SPF full form | Sender Policy Framework |
| DKIM full form | DomainKeys Identified Mail |
| DMARC full form | Domain-based Message Authentication, Reporting and Conformance |
| SHA full form | Secure Hash Algorithm |
| SIEM full form | Security Information and Event Management |
| CIA full form | Confidentiality, Integrity and Availability |
| SHA-256 output | 256 bits = 32 bytes = 64 hexadecimal characters |
| PageRank damping factor | Commonly 0.85 |
| Cosine similarity | Dot product divided by product of vector magnitudes |
| Jaccard coefficient | Intersection divided by union |
| MapReduce stages | Map → Shuffle and Sort → Reduce |
| Extractive summarization | Selects existing sentences |
| Abstractive summarization | Generates new sentences |
| Web crawler | Automatically discovers and downloads web pages |
| Event correlation | Analyses multiple events to identify patterns |
| Hash collision | Two different inputs produce the same hash |

---

# Important Mathematical Formula Sheet

### 1. TF-IDF

\[
TF(t,d)=\frac{f_{t,d}}{\text{Total terms in }d}
\]

\[
IDF(t)=\log\left(\frac{N}{DF(t)}\right)
\]

\[
\boxed{TFIDF(t,d)=TF(t,d)\times IDF(t)}
\]

### 2. Cosine Similarity

\[
\boxed{
\cos\theta=
\frac{\sum_{i=1}^{n}A_iB_i}
{\sqrt{\sum_{i=1}^{n}A_i^2}
\sqrt{\sum_{i=1}^{n}B_i^2}}
}
\]

### 3. Jaccard Coefficient

\[
\boxed{J(A,B)=\frac{|A\cap B|}{|A\cup B|}}
\]

### 4. PageRank

\[
\boxed{
PR(A)=\frac{1-d}{N}
+d\sum_{T_i\in In(A)}
\frac{PR(T_i)}{C(T_i)}
}
\]

### 5. Precision

\[
\boxed{Precision=\frac{TP}{TP+FP}}
\]

### 6. Recall

\[
\boxed{Recall=\frac{TP}{TP+FN}}
\]

### 7. F1 Score

\[
\boxed{
F1=2\times\frac{Precision\times Recall}
{Precision+Recall}
}
\]

### 8. SHA-256 Output Length

\[
256\text{ bits}=32\text{ bytes}=64\text{ hexadecimal characters}
\]

\[
\text{Possible output values}=2^{256}
\]

---

**Revision priority:** Focus first on Log Capturing and Event Correlation, XML Parsing, PageRank, TF-IDF, SHA-256, Cosine Similarity, Web Crawlers and MapReduce. These appeared repeatedly in the collected viva responses.
