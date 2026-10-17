"""CSDF Assignment 1 - Tracking emails and investigating email crimes.

Problem statement: analyse an e-mail header to trace the route of a message and
flag signs of spoofing/phishing (SPF/DKIM/DMARC results, From vs Return-Path
mismatch, Reply-To mismatch, relay hops and delays).

New libs used (all standard library): email (header parsing), re, datetime.

Input: the e-mail files listed in email_paths (data/genuine.eml, data/spoofed.eml) are read
and analysed. Change email_paths to test your own saved e-mail.
"""

import re
from datetime import datetime
from email import message_from_string
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

# e-mail files to analyse (relative to this folder, full paths also work)
email_paths = ["data/genuine.eml", "data/spoofed.eml"]


def domain(address):
    """Return the lower-case domain of an e-mail address."""
    return parseaddr(address)[1].rpartition("@")[2].lower()


def trace_route(msg):
    """Return relay hops oldest -> newest as (host, ip, time)."""
    hops = []
    for line in reversed(msg.get_all("Received", [])):
        line = " ".join(line.split())
        ip = re.search(r"\[?(\d{1,3}(?:\.\d{1,3}){3})\]?", line)
        host = re.search(r"from\s+(\S+)", line)
        when = parsedate_to_datetime(line.rsplit(";", 1)[1].strip())
        hops.append((host.group(1) if host else "?", ip.group(1) if ip else "?", when))
    return hops


def read_file(path):
    return (Path(__file__).parent / path).read_text(encoding="utf-8")


def analyse(raw):
    msg = message_from_string(raw)
    findings = []

    auth = (msg.get("Authentication-Results") or "").lower()
    for check in ("spf", "dkim", "dmarc"):
        found = re.search(check + r"=(\w+)", auth)
        result = found.group(1) if found else "missing"
        if result != "pass":
            findings.append(f"{check.upper()} result is '{result}'")

    from_dom, path_dom = domain(msg["From"]), domain(msg.get("Return-Path", ""))
    if path_dom and from_dom != path_dom:
        findings.append(f"From domain ({from_dom}) != Return-Path domain ({path_dom})")
    reply = msg.get("Reply-To")
    if reply and domain(reply) != from_dom:
        findings.append(f"Reply-To domain ({domain(reply)}) differs from From domain")

    hops = trace_route(msg)
    sent = parsedate_to_datetime(msg["Date"])
    if hops and (hops[-1][2] - sent).total_seconds() > 3600:
        findings.append("Message took more than 1 hour to deliver")
    return msg, hops, findings


def report(path):
    msg, hops, findings = analyse(read_file(path))
    print(f"=== {Path(path).name} ===")
    print(f"From: {msg['From']} | Subject: {msg['Subject']} | Message-ID: {msg['Message-ID']}")
    print("Route (origin -> destination):")
    for n, (host, ip, when) in enumerate(hops, 1):
        print(f"  hop {n}: {host:<22} {ip:<15} {when:%Y-%m-%d %H:%M:%S %z}")
    print("Verdict:", "SUSPICIOUS" if findings else "looks genuine")
    for f in findings:
        print("  -", f)
    print()


def main():
    for path in email_paths:
        report(path)


if __name__ == "__main__":
    main()
