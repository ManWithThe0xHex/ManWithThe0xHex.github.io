---
title: Gatekeeper
date: 2026-03-22 22:55:23 
categories: [ctf, picoctf, "2026", reverse Engineering]
tag: [picoctf, easy, reverse engineering, hex, logic flaw]
---

**1. File download:** [gatekeeper](/assets/Gatekeeper/gatekeeper)

![](/assets/Gatekeeper/images/description.png)

# File Analysis

Initial identification of the binary shows it is a standard 64-bit Linux executable. The fact that it is not stripped is helpful, as it likely contains debugging symbols that make analysis easier.

```shell
file gatekeeper
gatekeeper: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=f8be7d9d53fcf8763ed4b76fe8c98b23609085db, for GNU/Linux 3.2.0, not stripped
```

# Behavioral Analysis
To understand the program, we performed several manual executions test and check the output.
```shell
❯ ./gatekeeper
Enter a numeric code (must be > 999 ): 1000
Access Denied.
❯ ./gatekeeper
Enter a numeric code (must be > 999 ): 999
Too small.
❯ ./gatekeeper
Enter a numeric code (must be > 999 ): 10000
Too high.
```

After performing the analysis, we deduced that the number must be between 1000 and 9999.

# Source Code analysis
By reviewing the decompiled pseudocode( genrated by IDA), We notice that input must be between 1000 and 9999, with a specific constraint (v5) requiring exactly 3 digits.
```c
if ( v4 > 999 ){
    if ( v4 <= 9999 ){
        if ( v5 == 3 )
            reveal_flag();
        else
            puts("Access Denied.");
    } else  {
      puts("Too high.");
    }
} else {
    puts("Too small.");
}
```

# Vulnerability
We can not use decimal notation, as any decimal number over 999 requires at least 4 digits. To satisfy all conditions we use hexadecimal values (`FFF`).
```shell
❯ ./gatekeeper
Enter a numeric code (must be > 999 ): FFF
}XXXftc_oc_ipdXXcftc_oc_ipc_XXftc_oc_ipX_TGftc_oc_ip_xehftc_oc_ip_tigftc_oc_ipid_3ftc_oc_ip{FTCftc_oc_ipocipftc_oc_ip
```


# Flag reconstruction
The program return an obfuscated string, in revserse and using garbase sequence `pi_co_ctf`.
```shell
echo -n "}XXXftc_oc_ipdXXcftc_oc_ipc_XXftc_oc_ipX_TGftc_oc_ip_xehftc_oc_ip_tigftc_oc_ipid_3ftc_oc_ip{FTCftc_oc_ipocipftc_oc_ip"|rev| sed 's/pi_co_ctf//g'
```
