---
title: North-South
date: 2026-03-22 14:42:12 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [ctf, picoctf, web explotation, easy, location, end node, tor]
---

![](/assets/North-South/images/description.png)

# Web Recon
When we accessing the webapp, this show us the message *No flag in this region!*. This is a hint that if we access from diferente region we can get the flag!.
![](/assets/North-South/images/north-south.png)

# Analyzing nginx.conf
Reviewing the `nginx.conf` file reveals two applications running on the same server but on different ports.
By default  all standard traffic is routed to north instance, but if we connect from IS(isceland) we can access to south instance.
![](/assets/North-South/images/nginx.png)

# Configuring TOR for Regional Access
To spoof our location, we can use the TOR network to exit specifically from an Icelandic node.
1. Edit TOR file configuration `/etc/tor/torrc`
2. Append the follow lines to `torrc`.

```shell
ExitNodes {is}
StrictNodes 1
```

# Retrieving the Flag
After restarting the TOR service, we route a `curl` request through the local TOR SOCKS proxy
```shell
curl --socks5 127.0.0.1:9050 http://lonely-island.picoctf.net:60543/
picoCTF{g30_b453d_r0u71n9_xxxxxxxx}
```
