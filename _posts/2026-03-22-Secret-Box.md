---
title: Secret Box
date: 2026-03-22 14:43:44 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [picoctf, web explotation, medium, sql injection, insert]
---
![](/assets/Secret-Box/images/description.png)

# Web Recon
The application provides a user registration and login system.
![](/assets/Secret-Box/images/access.png)

Once authenticated, users can store private "secrets" in a personal vault. Initial testing confirmed that secrets are saved and displayed correctly.
![](/assets/Secret-Box/images/web_secrets.png)

# Source Code Analysis
A review of the backend source code revealed two critical security flaws:
1. **server.js:** The function responsible for saving secrets takes the user input and concatenates it directly into the SQL query without any sanitization or parameterization.

![](/assets/Secret-Box/images/sourcecode.png)

2. **db.js:** The database schema indicates that the flag is stored within the same `secrets` table, protected only by an `owner_id` column.
![](/assets/Secret-Box/images/db_secrets.png)

# Vulnerability Discovery (Information Leakage)
By submitting a malformed secret containing a single quote (`'`), we triggered a database error.
![](/assets/Secret-Box/images/quote.png)

The resulting error message leaked our UUID:
![](/assets/Secret-Box/images/owner_id.png)
# Exploitation (SQL Injection / Data Exfiltration)
Using the leaked `owner_id`, I crafted a **Stacked Query** payload. This payload closes the original `INSERT` statement and executes a new one that copies every entry in the `secrets` table (including the flag) and assigns them to our `owner_id`.

```sql
aaaaaaa');
insert into secrets(owner_id,content) SELECT 'bd3f7535-eebb-4a91-b436-26c3f4bee316',content FROM secrets;-- -
```

After submitting the payload, the application processed the injected `INSERT` statement. Upon refreshing the "My Secrets" page, the flag was visible among the newly added entries.
![](/assets/Secret-Box/images/flag.png)
