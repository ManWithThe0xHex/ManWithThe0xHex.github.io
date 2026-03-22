---
title: Fool The look out
date: 2026-03-22 14:43:32 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [picoctf, web explotation, easy, bruteforce, python, Rate Limiting bypass]
---

![](/assets/Fool-The-look-out/images/description.png)


# Web Recon
The target application features a standard login interface.
![](/assets/Fool-The-look-out/images/login.png)

# Analisis de código fuente
Initial testing and source code analysis revealed the server’s **Account Lockout Policy**:
- A maximum of **10 failed login attempts** is permitted.
- After reaching the 10 failed login attempts, the IP is blocked for **120 seconds (2 minutes)**.
![](/assets/Fool-The-look-out/images/sourcecode.png)


# Exploitation Strategy (Rate Limit Bypass)
Because the lockout duration is short and does not increase exponentially, the protection can be bypassed using a **time-throttled brute force attack**.
I developed a Python automation script, `brute_login.py`, to manage the timing of the requests. The script logic follows this loop:
1. Submit **10 login attempts** using credentials from the provided data dump.
2. Trigger a `sleep` function for **121 seconds** to allow the lockout timer to reset.
3. Resume the attack until a successful authentication is detected.
![](/assets/Fool-The-look-out/images/brute_code.png)

**Execution:**
```shell
❯ python brute_login.py
```
![](/assets/Fool-The-look-out/images/creds_found.png)


By automating the wait periods, the script successfully circumvented the "Lookout" mechanism. The valid credentials were identified, and upon logging in, the flag was retrieved.
![](/assets/Fool-The-look-out/images/flag.png)
