---
title: Old Sessions
date: 2026-03-22 14:42:38 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [picoctf, web explotation, easy, cookie]
---

![](/assets/Old-Sessions/images/description.png)

# Web Recon
The standard entry point of the application is a login/registration page.
![](/assets/Old-Sessions/images/login.png)


After creating a new account and authenticating, we inspected the page and discovered a suspicious comment pointing to a directory: `/sessions`..
![](/assets/Old-Sessions/images/comment.png)

# Vulnerability Discovery: Insecure Session Management
By navigating to the `/sessions` endpoint, we found a list of active session tokens. Among these entries, we identified a high-value cookie belonging to the **Administrator**.
![](/assets/Old-Sessions/images/sessions.png)

#  Exploitation (Session Hijacking)
To escalate our privileges and access the admin account, we followed these steps:
1. **Intercept/Edit:** Opened the browser's Developer Tools (F12) and navigated to the **Application** or **Storage** tab.
2. **Replace:** Replaced our current session cookie with the stolen **Administrator cookie**.
3. **Refresh:** Reloaded the page to authenticate as the admin.
![](/assets/Old-Sessions/images/replace_session.png)


the server validated the hijacked session, granting us access to the administrative dashboard where the flag was displayed.
![](/assets/Old-Sessions/images/flag.png)
