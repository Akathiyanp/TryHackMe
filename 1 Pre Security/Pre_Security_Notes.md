# Pre-Security Path Notes — TryHackMe

*Revision notes. Not a walkthrough. If you finished the path or just want to understand the concepts — this is for you.*

![img](https://miro.medium.com/v2/resize:fit:1105/1*OQZ1mjCEsvMXQMgYAYvYKg.png)Spent the last few weeks going through TryHackMe’s Pre-Security path. These are my notes — the way I actually write them, not the way a textbook would. Short, direct, no fluff. If something clicks differently for you, drop it in the comments.

![img](https://miro.medium.com/v2/resize:fit:947/1*Jk52TMxWqcBx_s05Z4KBZA.png)\## Module 1 — Introduction to Cybersecurity

## Offensive Security

Think like an attacker. Find the weakness before someone bad does — with permission.

**Scope** — exact systems + actions allowed. Outside scope = off limits. **Vulnerability** — weakness in a system **Exploit** — technique that takes advantage of that weakness **Enumeration** — collecting info (users, ports, services) to find weak spots **Dictionary attack** — trying a wordlist to guess passwords

```
gobuster dir --url http://example.com -w /usr/share/wordlists/dirbuster/directory-list.txt
```

→ finds hidden directories on a site

```
hydra -l admin -P passlist.txt www.site.thm http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect" -V
```

→ brute-forces login forms

## Defensive Security

**Prevention** — firewalls, antivirus, patching **Detection** — logs, alerts, SIEM **Mitigation** — isolate systems, block traffic, disable accounts mid-attack **Analysis** — what happened, how, which systems **Response + Improve** — recover, fix the root cause

Defender’s loop: threat anticipation → attack awareness → risk prioritisation → continuous adaptation

## Careers in Cybersecurity

**Red Team / Pen Tester** — simulate attacks, find flaws legally **SOC Analyst** — monitor, detect, respond in real time **Threat Intelligence** — research attacker behaviour, predict moves **Security Engineer** — build and maintain security infrastructure **Malware Analyst** — reverse-engineer malicious software **Incident Responder** — called in after something’s already gone wrong

## Module 2 — Network Fundamentals

## What is Networking?

**IPv4**–32-bit, 4 octets, ²³² addresses e.g. `86.157.52.21` **IPv6** — 128-bit, 8 groups, 2¹²⁸ addresses e.g. `2a00:22c4:a531:c500:425f:cce6:c36b:f64d` (created because IPv4 ran out) **MAC** — 12-char hex, hardware-level ID e.g. `a4:c3:f0:85:ac:2d` — first 6 = manufacturer, last 6 = device

**Ping** — ICMP packets, tests connection between two devices, measures round-trip time and packet loss

```
ping 8.8.8.8   /   ping google.com
```

## Intro to LAN

**Star** — all devices connect to a central switch/hub. Most common. Switch fails = everything fails. **Bus** — all share one backbone cable. Can’t handle heavy load. **Ring** — devices in a loop. One broken cable = whole ring down.

**Network address** — identifies the network e.g. `192.168.1.0` **Host address** — identifies a device e.g. `192.168.1.100` **Default gateway** — address devices use to send traffic *outside* their network (usually the router)

**ARP** — Address Resolution Protocol. Maintains a table of IP → MAC mappings.

- ARP Request — broadcasts “who has 192.168.1.100?” to all
- ARP Reply — that device responds with its MAC
- Attack: **ARP Spoofing** — fake replies poison the table

**DHCP** — auto-assigns IPs when a device joins a network. Flow = **DORA:**

1. Discover — device: “I need an IP”

2. Offer — server offers one

3. Request — device confirms

4. ACK — server locks it in

## OSI Model

7 layers. Every exam, every interview.

\# Layer What happens 7 Application DNS, HTTPS, SSH, FTP, SMTP 6 Presentation encryption, encoding, compression 5 Session connection setup, session handling, checkpoints 4 Transport TCP/UDP, ports, segmentation, reliability 3 Network IP addressing, routing (OSPF, RIP) — **packets** 2 Data Link MAC, frames, error detection (CRC), ARP — **frames** 1 Physical cables, electrical signals, binary

Bottom to top: **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

## Packets & Frames

**Packet** — Layer 3 data unit. IP header + payload. **Frame** — Layer 2 data unit. Packet + MAC address. **TTL** — timer on a packet. Decrements each hop. Hits 0 = dropped.

**TCP Three-Way Handshake:**

```
Client → SYN       (want to connect)
Server → SYN/ACK   (acknowledged)
Client → ACK       (let's go)
```

After: DATA transfers → FIN closes cleanly → RST = abrupt end (error/low resources)

**TCP** — reliable, ordered, error-checked → web, email, file transfer **UDP** — fast, no guarantee → streaming, gaming, DNS

TCP headers: Source IP, Destination IP, Source port, Destination port, Checksum, Flag, Data UDP headers: TTL, Source IP, Destination IP, Source port, Destination port, Data

## Extending Your Network

**Intranet** — private internal network, same org **Firewall:**

- Stateful — tracks the full connection, smarter
- Stateless — checks packets against rules only. No exact match = allows.

**VPN types:**

- **PPP** — auth + basic encryption between two direct endpoints. Non-routable.
- **PPTP** — tunnels PPP traffic across networks. Easy but weak encryption.
- **IPSec** — encrypts and authenticates IP packets at network layer. Strong, complex config.

Press enter or click to view image in full size

![img](https://miro.medium.com/v2/resize:fit:952/1*yAagFJosbDy1zfeHvnsb4w.png)\## Module 3 — How the Web Works

## DNS in Detail

Domain reads right → left: `admin.tryhackme.com`

- `com` → TLD
- `tryhackme` → SLD (Second Level Domain)
- `admin` → subdomain

**gTLD** — generic: `.com` `.org` `.net` **ccTLD** — country: `.in` `.uk` `.co.uk` Rules: `a-z`, `0-9`, `-` only. Each label ≤ 63 chars, total ≤ 253.

**DNS Records:**

- `A` → IPv4
- `AAAA` → IPv6
- `CNAME` → alias, one domain points to another (CDN, third-party services)
- `MX` → mail server + priority
- `TXT` → SPF, DMARC, domain verification

```
nslookup --type=CNAME shop.website.thm
nslookup --type=MX website.thm
nslookup --type=TXT website.thm
```

**DNS lookup flow:**

```
Local cache → Recursive DNS (ISP) → Root server → TLD server → Authoritative server
```

**Recursive** — finds the answer by asking around **Authoritative** — actually stores the record, gives the final answer **TTL** — how long the response is cached before querying again

DNS = Layer 7, uses UDP (fast) / TCP (large responses) Attacks: DNS Spoofing, Cache Poisoning, DNS Tunneling

## HTTP in Detail

**URL:** `https://tryhackme.com/room/index`

- Scheme — `https` (protocol used)
- Host — `tryhackme.com`
- Path — `/room/index` (resource requested, `/` = `index.html`)
- Localhost = `127.0.0.1`

**HTTP Methods (9 core):** `GET` — fetch, params in URL `POST` — send data, body carries payload `PUT` — create/replace `PATCH` — partial update `DELETE` — remove `HEAD` — headers only, no body `OPTIONS` — what methods does the server support? `CONNECT` — create a tunnel (proxies) `TRACE` — diagnostic, echoes request back

**Status codes:** `1xx` — info | `2xx` — success (200 OK, 201 Created) | `3xx` — redirect `4xx` — client error (403 Forbidden, 404 Not Found) | `5xx` — server error (500)

Response = **header** (metadata: content-type, cookies, cache) + **body** (HTML/JSON/file)

## How Websites Work

**HTML** — structure. Skeleton — headings, forms, links. **CSS** — style. Colours, fonts, layout. **JavaScript** — behaviour. Interaction, fetch data, validate forms without page reload. **Backend** — server-side logic + database. Processes logins, stores data.

Note: HTML comments can leak paths, JS files expose endpoints, unsanitised forms = injection targets.

## Putting It All Together

What happens when you type `tryhackme.com` and hit Enter:

```
DNS lookup → TCP handshake → TLS (HTTPS) → HTTP GET → Server responds → Browser renders
```

Every step = a potential attack surface.

## Module 4 — Computer Fundamentals

## Inside a Computer System

**CPU** — executes instructions. Core count + clock speed. **RAM** — temporary, volatile. Wiped on reboot. Holds active processes and keys in plain text while running. **Storage (HDD/SSD)** — persistent. OS, files, apps live here. **Motherboard** — connects everything. **GPU** — parallel processing. Also used in password cracking. **NIC** — Network Interface Card. Gives the machine its MAC address. **PSU** — converts mains power to what components need.

## Computer Types

**Desktop/Laptop** — general purpose, most common attack surface **Server** — headless, always-on, runs services (web, DB, DNS). High-value target. **Embedded systems** — routers, IoT, industrial controls. Often unpatched. **Mobile** — ARM, sandboxed apps. Vectors: Bluetooth, NFC, rogue apps. **VM** — software-emulated machine inside a real one. Isolated — good for malware analysis. **Cloud instances** — on-demand VMs/containers. Attack surface = misconfigurations.

## Client-Server Basics

**Client** — makes the request (browser, app) **Server** — receives and responds Communication over HTTP/HTTPS. Request = method + headers + optional body. Response = status + headers + body. `127.0.0.1` — loopback, refers to the device itself (localhost)

## Virtualisation Basics

One physical machine, multiple OS — made possible by a **hypervisor**.

**Type 1 (Bare Metal)** — directly on hardware, no host OS. More secure. Used in datacentres. **Type 2 (Hosted)** — runs on an existing OS. Easier setup (VirtualBox, VMware). What you use on your laptop. **Container** — isolated box for one app, shares the host OS kernel. Lighter than a VM. **Container Image** — template used to spin up containers. Pre-packed, reusable.

## Cloud Computing Fundamentals

**Public** — third-party provider, shared infra (AWS, Azure, GCP) **Private** — dedicated to one org, more control and security **Hybrid** — sensitive data on private, scalability on public

**IaaS** — hardware only. You manage OS + apps. e.g. AWS EC2 **PaaS** — hardware + OS. You manage apps + data. e.g. Heroku, Google App Engine **SaaS** — just use the app. You manage your data. e.g. Gmail, Zoom

![img](https://miro.medium.com/v2/resize:fit:917/1*Rm_UCaH70NALe6NAsqRjPA.png)\## Module 5 — Operating System Basics

## OS Introduction

**User space** — where apps run, make system calls for privileged access **Kernel space** — OS core + hardware drivers. Trusted, restricted.

OS manages: file system, processes, memory, users, devices.

macOS versions: Sonoma (14), Sequoia (15), Tahoe Embedded Linux: OpenWrt, Ubuntu Core, Yocto Project Real-Time OS: FreeRTOS, VxWorks, QNX

## Windows Basics

Users: **Guest** → **Standard** → **Administrator** Tools: Windows Defender (antivirus), Windows Security (dashboard), File Explorer, Task Manager

## Linux CLI Basics

```
ls -l              → list with permissions, size, owner
ls -al             → include hidden files
uname              → OS name
uname -a           → OS + kernel version + architecture
df -h              → disk space, human readable
find ~ -name filename.txt  → search entire system for file
```

## Windows CLI Basics

```
dir                → list files and directories
dir /a             → include hidden
dir /s task.txt    → search recursively
cd users\admin     → navigate with backslash
hostname           → machine name on the network
winver             → Windows version
whoami             → current user
systeminfo         → full system info
ipconfig           → network config
```

## Operating System Security

**CIA Triad:** **Confidentiality** — only authorised people access the data **Integrity** — data hasn’t been tampered with **Availability** — systems are up when needed

```
ssh username@ip              → e.g. ssh sammie@10.48.158.112
history                      → all commands run by this user
sudo openvpn filename.ovpn   → connect via VPN
ping IP                      → check if connection is live
```

## Module 6 — Software Basics

## Data Representation

Everything = 0s and 1s.

**Colours** — RGB, 256 × 256 × 256 = \~16 million colours **Hex** — each digit = 4 bits. Compact binary.

Yellow-green: `10100011 11101010 00101010` (binary) = `A3EA2A` (hex) = `(163, 234, 42)` (RGB) `AB` (hex) = `171` (decimal) = `10101011` (binary) = `253` (octal)

## Data Encoding

**ASCII** — 7-bit, 128 characters `0–31` control | `48–57` digits | `65–90` A–Z | `97–122` a–z Limitation: no non-English chars, no emoji

**Unicode** — unique code point for every character in every language. `U+0041` = A. v17.0 has \~157,000 chars.

**UTF** — how Unicode is stored:

- **UTF-8**–1–4 bytes, most common, backward-compatible with ASCII
- **UTF-16**–2 or 4 bytes, Windows/Java
- **UTF-32** — fixed 4 bytes, simple but wasteful

## Python — Quick Reference

```
print()          → output
input()          → take user input
int()            → string to integer
if / elif / else → conditionals
```

## JavaScript — Quick Reference

```
let x = 5;        // variable
const y = 10;     // constant
console.log(x);   // output to console
parseInt(value);  // string to integer
```

## SQL Basics

Table = spreadsheet. Columns = fields. Rows = records.

```
SELECT * FROM orders;
SELECT drink, price FROM orders;
SELECT * FROM orders WHERE drink = 'Tea';
SELECT * FROM orders ORDER BY price;
SELECT * FROM orders ORDER BY price DESC;
```

![img](https://miro.medium.com/v2/resize:fit:939/1*UnwWpAl1FmPYrD-7pCKx5Q.png)\## Module 7 — Attacks and Defences

## Cryptography

**Symmetric** — same key to encrypt and decrypt. Fast, but how do you share the key? Caesar cipher: key = 3, A→D, B→E `plaintext + algorithm + key = ciphertext` / reverse to decrypt

**Asymmetric** — solves the key-sharing problem. **Public key** — shared openly, used to encrypt **Private key** — never shared, used to decrypt

**HTTPS flow:**

```
Browser requests site → Server sends certificate (has public key)
→ Browser verifies CA signed it, not expired
→ Both agree on a shared symmetric key
→ All communication after = symmetric (faster)
```

**CA (Certificate Authority)** — trusted third party that signs certificates. Browsers ship with a built-in trusted CA list.

## Offensive Tools (Hacker’s side)

**gobuster** — enumerate hidden directories

```
gobuster dir --url http://example.com -w /usr/share/wordlists/dirbuster/directory-list.txt
```

**hydra** — brute-force credentials

```
hydra -l admin -P passlist.txt www.site.thm http-post-form "/login:username=^USER^&password=^PASS^:F=incorrect" -V
```

## Defensive Mindset

**Prevention** → **Detection** → **Mitigation** → **Analysis** → **Response + Improve**

*Threat anticipation* — map realistic attack paths before they happen *Attack awareness* — attacks follow stages, learn the frameworks (MITRE ATT&CK) *Risk prioritisation* — not all systems are equal risk. Focus on high-value targets. *Continuous adaptation* — defence is never done.

## Revision — Things Worth Memorising

**DORA** → DHCP: Discover, Offer, Request, ACK **OSI** → Physical, Data Link, Network, Transport, Session, Presentation, Application **TCP handshake** → SYN → SYN/ACK → ACK **TCP = reliable | UDP = fast** **Packet = Layer 3 | Frame = Layer 2** **DNS flow** → local cache → recursive → root → TLD → authoritative **Recursive finds, Authoritative stores** **Symmetric = same key | Asymmetric = public/private pair** **HTTPS** → asymmetric to agree on key → symmetric after **CIA** → Confidentiality, Integrity, Availability **ARP attack** → Spoofing | **DNS attack** → Cache Poisoning **Stateful firewall** = tracks full connection | **Stateless** = checks packets in isolation **IaaS/PaaS/SaaS** → you manage less as you go up **Type 1 hypervisor** = bare metal | **Type 2** = runs on existing OS **UTF-8** = most common encoding, ASCII-compatible

​

​ -by Prathmesh Murugan

https://medium.com/@murugan.prathmesh/tryhackme-pre-security-path-notes-i-wish-i-had-on-day-one-654a20458de0