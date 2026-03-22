---
title: Credential Stuffing
date: 2026-03-22 14:42:47 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [picoctf, easy, web explotation, bruteforce]
---

![](/assets/Credential-Stuffing/images/description.png)

# Reconnaissance
The challenge provides a remote service accessible via **Netcat (`nc`)**. Upon connecting, the service prompts for a username and password. Initial manual attempts with common credentials (e.g., `admin:password1`) were unsuccessful, indicating a more targeted approach was required.
![](/assets/Credential-Stuffing/images/recon.png)

# Information Gathering
The challenge provides a **data dump** (`creds-dump.txt`) containing a list of leaked usernames and passwords from a previous breach.
# Exploitation (Automated Attack)
To efficiently test the provided list, I developed a Python automation script, `brute.py`. The script performs the following actions:

1. **Iterates** through each entry in the provided credential list.
2. **Automates** the login process via a socket connection to the Netcat listener.
3. **Detects** the "success" string and stops execution once the valid pair is found.
![](/assets/Credential-Stuffing/images/brute_code.png)

**Execution Command:**
```shell
❯ python brute.py -t 4 creds-dump.txt
```

The script successfully identified the correct account. Upon the first successful login, the server returned the flag.
![](/assets/Credential-Stuffing/images/creds_found.png)
