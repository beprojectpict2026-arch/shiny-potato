# Mastering Log Pattern Extraction & CSV Data Wrangling with `awk`

When analyzing server logs or wrangling delimited data like CSV files in Linux, traditional utilities often hit limitations:
- `grep` searches full lines without field-level awareness.
- `cut` handles fixed delimiters but fails with irregular whitespace.
- Python or pandas can feel heavy when you need an immediate answer inside a terminal session.

Enter **`awk`** — a lightweight, field-aware pattern processing language built into virtually every Unix-like system. Whether you are debugging a web server in `/var/log`, filtering HTTP 5xx errors, or wrangling CSV reports, `awk` allows you to extract patterns, perform arithmetic, and reshape data in a single command line.

---

##  The Test Datasets

To test these commands in your WSL terminal, navigate to this directory (`cd /path/to/blogs/linux`). We will use two sample files:

### 1. `sample.log` (Web Server Access Log)
```text
192.168.1.10 - - [30/Oct/2026:10:15:20 +0000] "GET /api/v1/users HTTP/1.1" 200 1024
192.168.1.15 - - [30/Oct/2026:10:15:22 +0000] "POST /api/v1/auth/login HTTP/1.1" 401 256
192.168.1.10 - - [30/Oct/2026:10:15:30 +0000] "GET /index.html HTTP/1.1" 200 4096
192.168.1.20 - - [30/Oct/2026:10:16:01 +0000] "GET /api/v1/products HTTP/1.1" 500 512
192.168.1.25 - - [30/Oct/2026:10:16:15 +0000] "DELETE /api/v1/items/42 HTTP/1.1" 403 128
192.168.1.10 - - [30/Oct/2026:10:16:40 +0000] "GET /api/v1/products HTTP/1.1" 200 2048
192.168.1.30 - - [30/Oct/2026:10:17:02 +0000] "POST /api/v1/checkout HTTP/1.1" 503 1024
192.168.1.20 - - [30/Oct/2026:10:17:18 +0000] "GET /images/logo.png HTTP/1.1" 200 8192
192.168.1.15 - - [30/Oct/2026:10:17:45 +0000] "GET /api/v1/users HTTP/1.1" 404 180
192.168.1.10 - - [30/Oct/2026:10:18:05 +0000] "GET /api/v1/metrics HTTP/1.1" 200 512
```
* **Field Mapping**: `$1` = Client IP | `$4` = Timestamp | `$6` = HTTP Method | `$7` = Endpoint | `$9` = Status Code | `$10` = Bytes

### 2. `sample.csv` (Microservice Metric Report)
```csv
timestamp,service,status_code,response_time_ms,endpoint
2026-10-30 10:15:20,auth-service,200,45,/login
2026-10-30 10:15:22,auth-service,401,120,/login
2026-10-30 10:15:30,payment-service,500,850,/charge
2026-10-30 10:16:01,user-service,200,32,/profile
2026-10-30 10:16:15,order-service,200,68,/orders
2026-10-30 10:16:40,payment-service,503,1200,/charge
2026-10-30 10:17:02,user-service,404,25,/users/99
2026-10-30 10:17:18,order-service,200,55,/checkout
```

---

## 🛠️ The 6 Essential `awk` Commands

### 1. Column & Field Extraction (`$N` and `-F`)
* **What it does in brief:** Isolates specific columns by index from space-separated logs or custom-delimited files (like commas in CSVs with `-F','`), discarding unnecessary noise.
* **Code Use:**
```bash
# Extract Client IP ($1), Request Path ($7), and Status Code ($9) from web logs
awk '{print $1, $7, $9}' sample.log

# Extract Service ($2), Status Code ($3), and Endpoint ($5) from CSV
awk -F',' '{print $2, $3, $5}' sample.csv
```
* **Expected Output (`sample.log`):**
```text
192.168.1.10 /api/v1/users 200
192.168.1.15 /api/v1/auth/login 401
192.168.1.10 /index.html 200
192.168.1.20 /api/v1/products 500
192.168.1.25 /api/v1/items/42 403
192.168.1.10 /api/v1/products 200
192.168.1.30 /api/v1/checkout 503
192.168.1.20 /images/logo.png 200
192.168.1.15 /api/v1/users 404
192.168.1.10 /api/v1/metrics 200
```
> 📸 *Screenshot Placeholder: Column extraction running in WSL terminal*

---

### 2. Conditional Threshold Filtering (`$column >= value`)
* **What it does in brief:** Filters records using numerical or relational comparisons (e.g., isolate HTTP server errors `>= 500` or find requests with response latency over a certain threshold).
* **Code Use:**
```bash
# Filter only HTTP server error records (status code >= 500)
awk '$9 >= 500 {print $1, $6, $7, $9}' sample.log

# In CSV: Find requests where response_time_ms > 100 (skipping header with NR > 1)
awk -F',' 'NR > 1 && $4 > 100 {print $2, $4"ms", $5, $3}' sample.csv
```
* **Expected Output (`sample.log`):**
```text
192.168.1.20 "GET /api/v1/products 500
192.168.1.30 "POST /api/v1/checkout 503
```
> 📸 *Screenshot Placeholder: Error threshold filtering in WSL terminal*

---

### 3. Pattern Matching with Regular Expressions (`~` and `!~`)
* **What it does in brief:** Matches specific fields against regular expressions to isolate URLs, file types, or failure indicators without relying on an extra `grep` pipe.
* **Code Use:**
```bash
# Extract only API requests targeting either 'auth' or 'checkout'
awk '$7 ~ /\/api\/v1\/(auth|checkout)/ {print $1, $6, $7, $9}' sample.log

# Exclude static assets (.png, .html) to focus strictly on API traffic
awk '$7 !~ /\.(png|html)$/ {print $1, $7}' sample.log
```
* **Expected Output (Regex Match):**
```text
192.168.1.15 "POST /api/v1/auth/login 401
192.168.1.30 "POST /api/v1/checkout 503
```
> 📸 *Screenshot Placeholder: Regex pattern matching in WSL terminal*

---

### 4. Formatted Terminal Reports (`printf`)
* **What it does in brief:** Replaces unaligned raw logs with cleanly formatted, column-padded tables and custom headers for fast visual inspection.
* **Code Use:**
```bash
# Generate a clean, aligned summary table from raw log data
awk 'BEGIN {
    printf "%-15s | %-6s | %-6s | %s\n", "IP ADDRESS", "METHOD", "STATUS", "ENDPOINT";
    print "------------------------------------------------------------"
}
{
    gsub(/"/, "", $6);
    printf "%-15s | %-6s | %-6s | %s\n", $1, $6, $9, $7
}' sample.log
```
* **Expected Output:**
```text
IP ADDRESS      | METHOD | STATUS | ENDPOINT
------------------------------------------------------------
192.168.1.10    | GET    | 200    | /api/v1/users
192.168.1.15    | POST   | 401    | /api/v1/auth/login
192.168.1.10    | GET    | 200    | /index.html
192.168.1.20    | GET    | 500    | /api/v1/products
192.168.1.25    | DELETE | 403    | /api/v1/items/42
192.168.1.10    | GET    | 200    | /api/v1/products
192.168.1.30    | POST   | 503    | /api/v1/checkout
192.168.1.20    | GET    | 200    | /images/logo.png
192.168.1.15    | GET    | 404    | /api/v1/users
192.168.1.10    | GET    | 200    | /api/v1/metrics
```
> 📸 *Screenshot Placeholder: Formatted printf table in WSL terminal*

---

### 5. Frequency Counting with Associative Arrays (`count[$key]++`)
* **What it does in brief:** Groups and counts log entries in-memory (functioning like SQL `GROUP BY`), eliminating the need for chained `sort | uniq -c | sort -nr` pipelines.
* **Code Use:**
```bash
# Count total requests per Client IP and print highest volume callers first
awk '{ip_count[$1]++} END {for (ip in ip_count) printf "%-15s : %d requests\n", ip, ip_count[ip]}' sample.log | sort -k3 -nr

# Count frequency of each HTTP Status Code
awk '{status[$9]++} END {for (s in status) printf "HTTP %s : %d occurrences\n", s, status[s]}' sample.log
```
* **Expected Output (IP Breakdown):**
```text
192.168.1.10    : 4 requests
192.168.1.20    : 2 requests
192.168.1.15    : 2 requests
192.168.1.30    : 1 requests
192.168.1.25    : 1 requests
```
> 📸 *Screenshot Placeholder: Associative array grouping in WSL terminal*

---

### 6. Metric Aggregations & CSV Wrangling (`BEGIN`, `END`, & `OFS`)
* **What it does in brief:** Computes quantitative metrics (sums, averages) on the fly, and uses `OFS` (Output Field Separator) with `gsub()` to sanitize messy logs into clean CSV exports.
* **Code Use:**
```bash
# 6A: Compute total and average bandwidth (bytes transferred) across all requests
awk '{sum += $10; count++} END {
    printf "Total Requests : %d\nTotal Bytes    : %d bytes\nAverage Size   : %.2f bytes/request\n", count, sum, sum/count
}' sample.log

# 6B: Data Wrangling: Convert raw web logs into a sanitized CSV
awk 'BEGIN {OFS=","} {
    gsub(/[\[\]"]/, ""); 
    print $1, $4, $6, $7, $9, $10
}' sample.log > wrangled_output.csv && cat wrangled_output.csv
```
* **Expected Output (6A - Metrics Summary):**
```text
Total Requests : 10
Total Bytes    : 19468 bytes
Average Size   : 1946.80 bytes/request
```
* **Expected Output (6B - Sanitized CSV):**
```csv
192.168.1.10,30/Oct/2026:10:15:20,GET,/api/v1/users,200,1024
192.168.1.15,30/Oct/2026:10:15:22,POST,/api/v1/auth/login,401,256
192.168.1.10,30/Oct/2026:10:15:30,GET,/index.html,200,4096
...
```
> 📸 *Screenshot Placeholder: Aggregation and CSV conversion in WSL terminal*

---

## 📑 Quick Reference Cheat Sheet

| Task | Syntax Pattern | Example |
|---|---|---|
| **Delimiter Change** | `-F'<delimiter>'` | `awk -F',' '{print $1, $2}' file.csv` |
| **Row Filtering** | `$field <operator> <value>` | `awk '$9 >= 500' server.log` |
| **Regex Match** | `$field ~ /regex/` | `awk '$7 ~ /api/' server.log` |
| **Header / Footer** | `BEGIN { ... } END { ... }` | `awk 'END {print "Rows: " NR}' file.txt` |
| **Group Count** | `arr[$col]++` | `awk '{c[$1]++} END {for(k in c) print k, c[k]}'` |
| **CSV Output** | `OFS=","` | `awk 'BEGIN {OFS=","} {print $1, $2}'` |

---

## 🚀 How to Test in WSL

1. Open your WSL terminal:
   ```bash
   cd /mnt/d/shiny-potato/blogs/linux
   ```
2. Verify your test files:
   ```bash
   cat sample.log
   cat sample.csv
   ```
3. Run the commands one by one, take screenshots of your terminal output, and insert them into the placeholder spots above!
