# 0x5da AutoCTF — HackTheBox VPS Auto-Hack Toolkit

**Created by 0x5da** (Toasty / OsintToast / WoahToast)  
Exploit Developer & Security Engineer • OSINT • Pentesting Tools • CTF Automation  
[GitHub @0x5da](https://github.com/0x5da)

All code in this repo was written by 0x5da. Use only on systems you own or have explicit authorization to assess (e.g. HackTheBox).

---

## What This Is

A **single-file Python toolkit** (3800+ lines, 30 built-in exploit modules) that **automatically hacks VPS targets** on [HackTheBox](https://hs.hackthebox.com/). One command. Enter the IP. It does **everything** — scans every port, exploits every service, brute-forces every login, dumps every database, harvests every credential, and gives you a full loot report.

```
python3 htb_autoctf.py --auto 10.10.10.x
```

That's it. It hacks the box.

---

## How It Works

```
STEP 1 → You enter the target IP
STEP 2 → Full Auto-Hack runs ALL 30 tools in sequence:

  Phase 1  → Port scan (300 threads, 150+ ports)
  Phase 2  → Banner grab every open port
  Phase 3  → OS fingerprint (TTL + banner analysis)
  Phase 4  → Exploit matching against known CVEs
  Phase 5  → Web recon, dir bust, WordPress scan, credential harvest
  Phase 6  → FTP anonymous login + file listing
  Phase 7  → SSH brute force (20 users × 50 passwords)
  Phase 8  → SMB null session + share dump
  Phase 9  → SNMP community string brute force
  Phase 10 → Redis unauthenticated access + RCE
  Phase 11 → MySQL/PostgreSQL brute force + full database dump
  Phase 12 → MongoDB unauthenticated access + data exfil
  Phase 13 → Memcached item dump + credential extraction
  Phase 14 → Docker API exploit + host filesystem mount
  Phase 15 → VNC brute force (DES challenge-response)
  Phase 16 → DNS reconnaissance

STEP 3 → Full loot report:
  • All open ports and services
  • OS fingerprint
  • All vulnerabilities with CVE IDs
  • All harvested credentials (SSH, DB, Redis, web, API keys)
  • All captured flags
  • All RCE vectors
  • Suggested next steps
  • JSON report saved to disk
```

---

## The 30 Built-In Tools

Every tool is **custom-written from scratch** by 0x5da — no wrappers, no API calls, all raw Python.

### Reconnaissance (6 tools)

| # | Tool | What It Does |
|---|------|-------------|
| 1 | **TCP Port Scanner** | 300-thread connect scan, top 150+ ports or custom range |
| 2 | **UDP Port Scanner** | Protocol-specific probes (DNS, SNMP, NTP) |
| 3 | **Banner Grabber** | Service-specific probes per port, version extraction |
| 4 | **OS Fingerprinter** | TTL analysis + banner keyword matching |
| 5 | **DNS Recon** | A/AAAA/MX/NS/TXT/SOA lookups + zone transfer attempts |
| 6 | **Subdomain Enumerator** | Multi-threaded DNS brute force, 50+ subdomains |

### Web Exploitation (9 tools)

| # | Tool | What It Does |
|---|------|-------------|
| 7 | **Directory Buster** | 100+ paths, configurable extensions (.php, .bak, etc.) |
| 8 | **Web Recon** | robots.txt, sitemap.xml, headers, HTML comments, forms |
| 9 | **Tech Fingerprinter** | Server, framework, CMS from headers/cookies/HTML |
| 10 | **SQL Injection Scanner** | Error-based + boolean-blind + time-based SQLi |
| 11 | **XSS Scanner** | Reflected XSS + SSTI detection, 14 payloads |
| 12 | **LFI Scanner** | 18 path traversal payloads, null bytes, PHP wrappers |
| 13 | **Command Injection Scanner** | Output-based + time-based, 15 payloads |
| 14 | **WordPress Scanner** | Version, users (REST API + author), 30 plugins, security checks |
| 15 | **Web Credential Harvester** | Scrapes .env, .git, config files, backups for passwords, API keys, flags |

### VPS & Network Exploitation (10 tools)

| # | Tool | What It Does |
|---|------|-------------|
| 16 | **FTP Exploit** | Anonymous login, file listing, writable directory detection |
| 17 | **SMB Enumerator** | Null session, share listing, RPC user enumeration |
| 18 | **SNMP Enumerator** | Raw SNMP v1 packets, 18 community strings, system info |
| 19 | **SSH Brute Forcer** | Paramiko dictionary attack, rate limiting, 20×50 combos |
| 20 | **Redis Exploit** | No-auth check, key dump, config extraction, webshell write, SSH key injection |
| 21 | **Database Brute + Dump** | MySQL/PostgreSQL default creds, full DB/table/user/hash dump |
| 22 | **MongoDB Exploit** | Wire protocol probe, database/collection enum, user credential dump |
| 23 | **Memcached Dump** | Stats extraction, slab enumeration, full key-value dump |
| 24 | **Docker API Exploit** | Unauthenticated API access, container exec, host filesystem mount |
| 25 | **VNC Brute Forcer** | Raw RFB protocol handshake, DES challenge-response brute force |

### Crypto, Utilities & Post-Exploitation (5 tools)

| # | Tool | What It Does |
|---|------|-------------|
| 26 | **Hash Cracker** | MD5/SHA1/SHA256/SHA512/NTLM identification + dictionary attack |
| 27 | **Crypto Toolkit** | Base64/Hex/URL/ROT13/Binary encode-decode + Caesar brute force |
| 28 | **Reverse Shell Generator** | 18 payloads: Bash, Python, PHP, Perl, Ruby, NC, PowerShell, etc. |
| 29 | **PrivEsc Enumerator** | SUID/capabilities/sudo/cron/writable files/Docker/password hunting |
| 30 | **VPS Exploit Matcher** | Matches banners against 21 known CVEs (Shellshock, Drupalgeddon, etc.) |

---

## Full Auto-Hack Engine

The **Full Auto-Hack** is the main feature. Option `[1]` in the menu or `--auto` from CLI.

It chains all 30 tools in the correct order based on what it discovers. Every open port triggers the right exploit module. Every credential found is logged. Every flag is captured.

At the end you get:

```
  ▄▀▄▀▄  ATTACK COMPLETE  ▄▀▄▀▄

  Target:          10.10.10.x (10.10.10.x)
  OS Guess:        Linux (Ubuntu/Debian)
  Open Ports:      7
  Vulns Found:     4
  Creds Found:     12
  RCE Vectors:     2
  Flags Found:     1
  Time Elapsed:    47.3s

  ── Harvested Credentials & Secrets ──
    ● [ssh_login]       admin:P@ssw0rd
    ● [mysql_login]     root:(blank)
    ● [redis_data]      session_token=eyJhbGci...
    ● [db_password]     DB_PASSWORD=s3cretDbPwd!
    ● [api_key]         APIKEY=sk_live_abcdef123456
    ● [htb_flag]        HTB{y0u_g0t_th3_fl4g}
    ...

  ── RCE Vectors ──
    ● Redis webshell write: /var/www/html/0x5da_test.php
    ● Docker host filesystem mount → full compromise
```

---

## Install

```bash
git clone https://github.com/0x5da/0x5da-AutoCTF.git
cd 0x5da-AutoCTF
pip install -r requirements.txt
python3 htb_autoctf.py
```

### Requirements

- Python 3.6+
- **Core:** Runs on standard library alone
- **Optional:** `paramiko` (SSH brute), `pymysql` (MySQL dump), `pycryptodome` (VNC brute)
- **System tools (optional):** `smbclient`, `rpcclient`, `dig`, `psql`, `mongosh`

---

## Usage

### Full Auto-Hack (One Command)

```bash
python3 htb_autoctf.py --auto 10.10.10.x
```

Runs all 30 tools. No prompts. Full loot report at the end.

### Interactive Mode

```bash
python3 htb_autoctf.py
```

```
  ────────────────────────────────────────────────────
    0x5da AutoCTF — Main Menu
  ────────────────────────────────────────────────────

    [1]  FULL AUTO-HACK         All 30 tools, automatic, everything
    [2]  Reconnaissance          Port scan, banners, OS, DNS
    [3]  Web Exploitation        DirBust, SQLi, XSS, LFI, CMDi, WP, Creds
    [4]  Network & VPS Exploit   FTP, SMB, SSH, Redis, DB, Mongo, Docker, VNC
    [5]  Crypto & Utilities      Hashes, encoding, shells, privesc, exploits
    [6]  Set Target
    [0]  Exit
```

---

## Embedded Wordlists

| Wordlist | Count | Used By |
|----------|-------|---------|
| TCP ports | 150+ | Port scanner |
| UDP ports | 13 | UDP scanner |
| Web directories | 100+ | Directory buster |
| Sensitive file paths | 57 | Credential harvester |
| Credential regex patterns | 16 | Credential harvester |
| Subdomains | 50+ | Subdomain enumerator |
| Usernames | 20 | SSH/DB brute force |
| Passwords | 50+ | SSH/DB/VNC/Redis brute force |
| Database credentials | 23 | MySQL/PostgreSQL brute force |
| SQLi payloads | 22 | SQL injection scanner |
| XSS payloads | 14 | XSS scanner |
| LFI payloads | 18 | LFI scanner |
| CMDi payloads | 15 | Command injection scanner |
| SNMP communities | 18 | SNMP enumerator |
| WP plugins | 30 | WordPress scanner |
| Known CVEs | 21 | Exploit matcher |

---

## Branding & Integrity

All code authored by **0x5da (Toasty / OsintToast / WoahToast)**. Embedded integrity checks and author signatures throughout.

```
__author__    = "0x5da"
__aliases__   = "Toasty / OsintToast / WoahToast"
__signature__ = "0x5da-AutoCTF-Toasty"
__codename__  = "WoahToast"
__version__   = "2.0.0"
```

---

## Legal

**This tool is for authorized security testing only.**

- Only use on systems you own or have explicit written permission to test
- HackTheBox machines are intentionally vulnerable — authorized use
- The author (0x5da) is not responsible for any misuse
- Unauthorized access to computer systems is illegal

---

## Credits

**Created by 0x5da** (Toasty / OsintToast / WoahToast)  
All 30 tools, the Full Auto-Hack engine, embedded wordlists, CVE database, and exploit logic — written from scratch. 3800+ lines of pure Python.

Built for the HackTheBox community. Stay frosty.
