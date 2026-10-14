"""CSDF Assignment 5 - Log capturing and event correlation.

Problem statement: capture log lines from several sources (SSH auth log,
firewall log, web server log), normalise them into common events and correlate
them by source IP within a time window to detect attack patterns.

New libs used (all standard library): re (parsing), datetime, collections.

Driver: a sample multi-source log is embedded below; the program parses it,
runs three correlation rules and prints the alerts. No input is taken at runtime.
"""

import re
from collections import defaultdict
from datetime import datetime, timedelta

SAMPLE_LOGS = """\
auth     2026-10-14 09:00:01 sshd Failed password for root from 203.0.113.50 port 4001
auth     2026-10-14 09:00:03 sshd Failed password for admin from 203.0.113.50 port 4002
auth     2026-10-14 09:00:05 sshd Failed password for root from 203.0.113.50 port 4003
auth     2026-10-14 09:00:07 sshd Failed password for user from 203.0.113.50 port 4004
auth     2026-10-14 09:00:09 sshd Failed password for root from 203.0.113.50 port 4005
auth     2026-10-14 09:00:12 sshd Accepted password for root from 203.0.113.50 port 4006
firewall 2026-10-14 08:58:00 DROP src=198.51.100.9 dst=10.0.0.5 dport=22
firewall 2026-10-14 08:58:01 DROP src=198.51.100.9 dst=10.0.0.5 dport=23
firewall 2026-10-14 08:58:02 DROP src=198.51.100.9 dst=10.0.0.5 dport=80
firewall 2026-10-14 08:58:03 DROP src=198.51.100.9 dst=10.0.0.5 dport=443
firewall 2026-10-14 08:58:04 DROP src=198.51.100.9 dst=10.0.0.5 dport=3306
firewall 2026-10-14 09:05:00 ALLOW src=203.0.113.50 dst=10.0.0.5 dport=443
web      2026-10-14 09:06:10 GET /login 200 203.0.113.50
web      2026-10-14 09:06:15 GET /admin' OR '1'='1 500 203.0.113.50
web      2026-10-14 09:07:00 GET /index.html 200 192.0.2.77
"""

FIELDS = {
    "auth": re.compile(r"(?P<time>\S+ \S+) sshd (?P<result>Failed|Accepted) password for (?P<user>\S+) from (?P<ip>\S+)"),
    "firewall": re.compile(r"(?P<time>\S+ \S+) (?P<action>DROP|ALLOW) src=(?P<ip>\S+) dst=\S+ dport=(?P<port>\d+)"),
    "web": re.compile(r"(?P<time>\S+ \S+) (?P<method>GET|POST) (?P<path>.+) (?P<status>\d{3}) (?P<ip>\S+)$"),
}


def capture(text):
    """Parse raw lines of every source into normalised event dicts."""
    events = []
    for line in text.splitlines():
        source, rest = line.split(None, 1)
        match = FIELDS[source].match(rest)
        if match:
            event = match.groupdict()
            event["source"] = source
            event["time"] = datetime.strptime(event["time"], "%Y-%m-%d %H:%M:%S")
            events.append(event)
    return sorted(events, key=lambda e: e["time"])


def by_ip(events):
    groups = defaultdict(list)
    for e in events:
        groups[e["ip"]].append(e)
    return groups


def correlate(events):
    """Apply correlation rules per source IP and return a list of alerts."""
    alerts = []
    for ip, evs in by_ip(events).items():
        fails = [e for e in evs if e["source"] == "auth" and e["result"] == "Failed"]
        success = [e for e in evs if e["source"] == "auth" and e["result"] == "Accepted"]
        drops = [e for e in evs if e["source"] == "firewall" and e["action"] == "DROP"]
        web = [e for e in evs if e["source"] == "web"]

        # Rule 1: >= 5 failed logins within 30 s -> brute force
        if len(fails) >= 5 and fails[-1]["time"] - fails[0]["time"] <= timedelta(seconds=30):
            alerts.append((ip, "HIGH", f"Brute force: {len(fails)} failed SSH logins in 30 s"))
            # Rule 2: brute force followed by success -> probable compromise
            if success and success[0]["time"] > fails[-1]["time"]:
                alerts.append((ip, "CRITICAL", "Successful login right after brute force: account likely compromised"))
        # Rule 3: >= 5 distinct ports dropped by firewall -> port scan
        if len({e["port"] for e in drops}) >= 5:
            alerts.append((ip, "MEDIUM", f"Port scan: {len({e['port'] for e in drops})} distinct ports blocked"))
        # Rule 4: injection pattern in web request after earlier suspicious activity
        if fails and any("'" in e["path"] for e in web):
            alerts.append((ip, "HIGH", "SQL-injection style request from an IP that also attacked SSH"))
    return alerts


def main():
    events = capture(SAMPLE_LOGS)
    print(f"Captured {len(events)} events from {len({e['source'] for e in events})} sources")
    for ip, evs in by_ip(events).items():
        print(f"  {ip:<15} {len(evs)} events")
    print("\nCorrelation alerts:")
    for ip, severity, message in sorted(correlate(events), key=lambda a: a[0]):
        print(f"  [{severity:<8}] {ip:<15} {message}")


if __name__ == "__main__":
    main()
