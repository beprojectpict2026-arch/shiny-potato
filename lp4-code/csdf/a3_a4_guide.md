# CSDF Assignments 3 and 4: Implementation Guide

These two assignments need real hardware, so there is no runnable Python file for them. This guide covers the setup, hardware, tools and the steps for the journal and demo. Only do this on equipment you own, in an isolated lab.

---

## Assignment 3: Detect and block Wi-Fi password-cracking attempts

**Problem statement:** A person on a nearby road tries to crack the Wi-Fi password to use the IP printer. Detect the attempt and prohibit access, using an IEEE 802.11 adapter and an access point.

### Hardware required

| Item | Purpose |
|---|---|
| Wireless access point or router (OpenWrt/DD-WRT) **or** a Linux PC running `hostapd` | The protected network |
| IP printer (or a Raspberry Pi/PC pretending to be one on port 9100) | The resource to protect |
| USB Wi-Fi adapter that supports **monitor mode** and packet injection (Atheros AR9271, Ralink RT3070 or Realtek RTL8812AU chipsets) | The sensor/IDS |
| Laptop 1 | Monitor/IDS machine (Linux, Kali or Ubuntu) |
| Laptop 2 or phone | The "attacker" test client; it only repeatedly tries wrong passphrases on your own AP |

### Software

`hostapd`, `dnsmasq`, `aircrack-ng` suite (`airmon-ng`, `airodump-ng`), `wireshark`/`tshark`, `iw`, `python3` with `scapy`, `iptables`/`ebtables`.

### Scenario setup

1. **Build the AP** (on a Linux PC with a Wi-Fi card) with `hostapd`:
   ```
   interface=wlan0
   ssid=PICT-LAB
   hw_mode=g
   channel=6
   wpa=2
   wpa_passphrase=<strong passphrase>
   wpa_key_mgmt=WPA-PSK
   rsn_pairwise=CCMP
   ieee80211w=1                 # protected management frames (stops forged deauth)
   macaddr_acl=0
   deny_mac_file=/etc/hostapd/deny.mac
   ```
   Give clients IPs with `dnsmasq` and put the printer on a fixed IP, e.g. `192.168.10.50`.
2. **Put the monitor adapter in monitor mode:** `sudo airmon-ng start wlan1`, then verify with `iw dev`.
3. **Simulate the attacker (test only):** from Laptop 2, repeatedly try to join `PICT-LAB` with wrong passphrases. Each try produces an authentication/association and EAPOL handshake that fails.

### Detection logic (what the program does)

Sniff 802.11 frames on the monitor interface and keep a per-source-MAC counter in a sliding time window (for example 60 s):

* Count **repeated failed WPA handshakes** (EAPOL message 1 and 2 seen without message 4) and repeated authentication/association requests per MAC.
* Count **deauthentication/disassociation frames** (a sign of handshake-capture attacks).
* **Alert** when a MAC exceeds the threshold (for example 5 failed handshakes in 60 s).
* **Respond** by appending the MAC to `/etc/hostapd/deny.mac` and running `hostapd_cli deny_acl ADD_MAC <mac>` (or `iptables`/`ebtables` rules on the AP to drop it). The printer's firewall or VLAN rules should allow only authenticated clients.

In Python the sniffing part is `scapy.sniff(iface="wlan1mon", prn=handler)`, inspecting `Dot11Auth`, `Dot11AssoReq`, `Dot11Deauth` and `EAPOL` layers. Everything else is dictionary counting plus a call to `hostapd_cli`.

### Hardening to mention in the journal

* WPA3-SAE (resists offline dictionary attacks), long random passphrase, WPS disabled.
* 802.11w (PMF) enabled, MAC filtering as a secondary measure only (MACs can be spoofed).
* Put the printer on a separate VLAN with firewall rules; enable the printer's own access control.

### What to show in the demo

Screenshots of: `hostapd` running, monitor mode on, the failed attempts in Wireshark, the alert printed, the MAC added to the deny list, and the attacker's next attempt being rejected.

---

## Assignment 4: Recover permanently deleted files and deleted partitions

**Problem statement:** Write a computer forensic application that recovers permanently deleted files and deleted partitions.

### Hardware required

* Linux PC (Ubuntu/Kali) with at least 8 GB RAM.
* A **spare USB drive or SD card** (1-8 GB) as the test media, **or** no extra hardware if you use a loop-mounted disk image (recommended for repeatable results).
* A hardware or software **write blocker** is used on real evidence drives. Work only on a bit-for-bit copy.

### Software

`dd`/`ddrescue`, `losetup`, `fdisk`/`parted`, `mkfs.ext4`/`mkfs.vfat`, **The Sleuth Kit** (`mmls`, `fls`, `icat`, `tsk_recover`), `testdisk` (partition recovery), `photorec`/`foremost` (file carving), `sha256sum`, `python3`.

### Part A: Recover deleted files

1. **Create the test media:** `dd if=/dev/zero of=disk.img bs=1M count=64`, then `mkfs.ext4 disk.img`, `sudo mount -o loop disk.img /mnt/t`.
2. Copy sample files (a few JPEGs, PDFs, text files) and record `sha256sum` of each. Delete them with `rm`, then unmount.
3. **Acquire an image** of the media (`dd if=disk.img of=evidence.img`) and hash it. All work continues on the copy.
4. **Recover:**
   * Filesystem aware: `fls -rd evidence.img` lists deleted entries, `icat evidence.img <inode> > file`, or `tsk_recover -e evidence.img out/`.
   * Signature carving (works when metadata is gone): `foremost -i evidence.img -o out/` or `photorec evidence.img`.
5. Compare `sha256sum` of recovered files with the originals to prove integrity.

**How it works (journal theory):** deleting a file only removes the directory entry and marks its inode/blocks free. The data stays until overwritten. Carving finds files by header/footer signatures (JPEG `FF D8 FF` ... `FF D9`, PNG `89 50 4E 47` ... `IEND`, PDF `%PDF` ... `%%EOF`).

**Python program outline:** open the image as bytes, scan for known header signatures, read until the matching footer (or a maximum size), write each hit to `recovered_N.ext`, and print offset, size and SHA-256. This is about 40 lines with only `hashlib` and `re`.

### Part B: Recover deleted partitions

1. Create the layout: `parted disk.img mklabel msdos mkpart primary ext4 1MiB 30MiB mkpart primary ext4 30MiB 60MiB`, attach with `sudo losetup -fP disk.img`, format both partitions and put files on them.
2. Note the table with `mmls disk.img`, **delete one partition** with `fdisk` (this only edits the partition table), then run `mmls` again to see it vanish.
3. **Recover:** `testdisk disk.img`, then Analyse, Quick Search/Deeper Search, which finds the old filesystem boundaries from their signatures (for example the ext4 magic `0xEF53` at offset 1080 of the partition), then Write to restore the table.
4. Mount the recovered partition and verify the files by hash.

**Python option:** read the MBR (first 512 bytes), parse the four 16-byte partition entries (type, start LBA, sector count) and print them. After deletion the entry is zeroed. Scan sector by sector for filesystem signatures to rebuild the start offset and restore the entry (take the size from the filesystem header).

### Forensic good practice to mention

Work on copies, hash before and after (integrity), keep a chain-of-custody log, use a write blocker on physical evidence, and note that SSD TRIM and overwritten blocks can make recovery impossible.
