"""CSDF Assignment 1 - Tracking emails and investigating email crimes.

Problem statement: analyse an e-mail header to trace the route of a message and
flag signs of spoofing/phishing (SPF/DKIM/DMARC results, From vs Return-Path
mismatch, Reply-To mismatch, relay hops and delays).

New libs used (all standard library): email (header parsing), re, datetime.

Driver: two embedded sample headers (one genuine, one spoofed) are analysed.
No input is taken at runtime.
"""

import re
from datetime import datetime
from email import message_from_string
from email.utils import parseaddr, parsedate_to_datetime

GENUINE = """\
Received: from mail-out.example.com (mail-out.example.com [203.0.113.10])
 by mx.pict.edu (Postfix) with ESMTPS id A1; Tue, 13 Oct 2026 10:00:05 +0530
Received: from [192.168.1.5] (unknown [198.51.100.7])
 by mail-out.example.com with ESMTPSA id B2; Tue, 13 Oct 2026 10:00:01 +0530
Authentication-Results: mx.pict.edu; spf=pass smtp.mailfrom=example.com;
 dkim=pass header.d=example.com; dmarc=pass header.from=example.com
From: Alice <alice@example.com>
Return-Path: <alice@example.com>
To: student@pict.edu
Subject: Lab schedule
Date: Tue, 13 Oct 2026 10:00:00 +0530
Message-ID: <abc123@example.com>

Hello
"""

SPOOFED = """\
Received: from unknown (HELO mail.bank.com) (45.33.32.156)
 by mx.pict.edu with SMTP; Tue, 13 Oct 2026 03:00:00 +0530
Received: from sender.bad-host.ru ([45.33.32.156])
 by relay.bad-host.ru; Mon, 12 Oct 2026 21:00:00 +0530
Authentication-Results: mx.pict.edu; spf=fail smtp.mailfrom=bad-host.ru;
 dkim=none; dmarc=fail header.from=bank.com
From: "Bank Support" <support@bank.com>
Return-Path: <bounce@bad-host.ru>
Reply-To: refunds@gmail-secure.net
To: student@pict.edu
Subject: Urgent: verify your account
Date: Mon, 12 Oct 2026 21:00:00 +0530
Message-ID: <zzz@bad-host.ru>

Click here
"""


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


def report(title, raw):
    msg, hops, findings = analyse(raw)
    print(f"=== {title} ===")
    print(f"From: {msg['From']} | Subject: {msg['Subject']} | Message-ID: {msg['Message-ID']}")
    print("Route (origin -> destination):")
    for n, (host, ip, when) in enumerate(hops, 1):
        print(f"  hop {n}: {host:<22} {ip:<15} {when:%Y-%m-%d %H:%M:%S %z}")
    print("Verdict:", "SUSPICIOUS" if findings else "looks genuine")
    for f in findings:
        print("  -", f)
    print()


def main():
    report("Sample 1 (genuine)", GENUINE)
    report("Sample 2 (spoofed)", SPOOFED)


if __name__ == "__main__":
    main()
