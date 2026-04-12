# Edge Case Catalog
## Comprehensive test values for systematic QA data generation

Use this catalog when generating "stress data" or edge-case datasets. Include these values deliberately to expose boundary and encoding bugs.

---

## Strings / Text Fields

### Length boundaries
```
""                          # Empty string
" "                         # Single space
"A"                         # Single character
"AB"                        # Two characters
"x" * 254                   # Common email max
"x" * 255                   # Common VARCHAR(255) limit
"x" * 256                   # One over 255 — often fails
"x" * 1000                  # Long but not absurd
"x" * 65535                 # MySQL TEXT limit
```

### Special characters
```
"O'Brien"                   # Apostrophe (SQL injection classic)
""; DROP TABLE users; --    # SQL injection attempt
"<script>alert(1)</script>" # XSS attempt
"&lt;b&gt;bold&lt;/b&gt;"  # HTML entities
"Hello\nWorld"              # Newline in string
"Hello\tWorld"              # Tab character
"Hello\0World"              # Null byte
"C:\\Users\\test"           # Windows path
"/etc/passwd"               # Unix path
```

### Unicode and internationalization
```
"مرحبا بالعالم"             # Arabic (RTL)
"שלום עולם"                 # Hebrew (RTL)
"你好世界"                   # Chinese (CJK)
"Héllo Wörld"               # Latin with diacritics
"日本語テスト"               # Japanese
"한국어 테스트"              # Korean
"🚀💯🎉🔥"                  # Emoji
"𝕳𝖊𝖑𝖑𝖔"                   # Mathematical bold (unusual Unicode block)
"Ａｌｌ　ｆｕｌｌ　ｗｉｄｔｈ"  # Fullwidth ASCII
"‮esreveR"                  # Right-to-left override character
"café"                      # NFD vs NFC normalization (é as e + combining)
```

### Names (personal)
```
"O'Reilly"                  # Apostrophe
"van der Berg"              # Multi-part with spaces
"张伟"                      # Chinese name
"Müller"                    # German umlaut
"Ó'Briain"                  # Irish with fada
"Al"                        # Very short first name
"X Æ A-12"                  # Unusual (but real)
"María-José"                # Hyphenated with accent
```

---

## Numbers

### Integer boundaries
```
0
-1
1
-2147483648     # INT32 min
2147483647      # INT32 max
2147483648      # INT32 overflow
-9223372036854775808   # INT64 min
9223372036854775807    # INT64 max
```

### Float / decimal
```
0.0
-0.0
0.1             # Classic float imprecision (0.1 + 0.2 ≠ 0.3)
1.0 / 3.0       # Repeating decimal
99.99
100.00
999999999.99    # Large price
0.001           # Very small
1e308           # Near float max
```

### Currency / prices
```
0.00            # Free item
0.01            # Minimum price (cent)
9.99            # Charm pricing
10.00
99.99
1000.00
9999999.99      # Large but valid
-1.00           # Negative (refund scenarios)
```

---

## Dates and Times

### Boundary dates
```
1900-01-01      # Historical minimum
1969-12-31      # Day before Unix epoch
1970-01-01      # Unix epoch
1999-12-31      # Pre-Y2K
2000-01-01      # Y2K
2000-02-29      # Leap day (year 2000 IS a leap year)
2001-02-29      # Invalid — 2001 not a leap year
2038-01-19      # Unix 32-bit timestamp overflow
2099-12-31      # Far future
9999-12-31      # Maximum date in most DBs
```

### Timezone edge cases
```
2024-03-10T02:30:00-05:00   # During US DST spring-forward (time doesn't exist)
2024-11-03T01:30:00-04:00   # During US DST fall-back (time exists twice)
2024-03-31T01:30:00+00:00   # During EU DST spring-forward
"2024-01-15T00:00:00Z"      # UTC midnight
"2024-01-15T23:59:59+14:00" # UTC+14 (easternmost timezone)
```

---

## Email Addresses

### Valid but unusual
```
"user+tag@example.com"          # Subaddressing
"user.name@example.co.uk"       # Two-part TLD
"user@münchen.de"               # Unicode domain
"user@xn--mnchen-3ya.de"        # Punycode equivalent
"a@b.io"                        # Very short
"very.long.email.address.that.is.valid.but.unusual@subdomain.example.com"
"user@[192.168.1.1]"            # IP address domain
"\"quoted string\"@example.com" # Quoted local part (valid per RFC 5321)
```

### Boundary lengths
```
"a@b.cc"        # Near-minimum valid
"x" * 64 + "@example.com"   # Local part at max (64 chars)
"user@" + "x" * 245 + ".com"  # Total near 254 char max
```

---

## Phone Numbers

```
"+1 (555) 000-0000"         # US format with formatting
"5550000000"                # US digits only
"+44 20 7946 0958"          # UK format
"+81-3-0000-0000"           # Japan format
"+86 10 0000 0000"          # China format
"00447946000000"            # International with 00 prefix
"911"                       # Emergency number (test validation)
"1234567890123456"          # Too long
""                          # Empty (optional field)
```

---

## Addresses

```
# Very long
"123456789 Superlongstreetname Boulevard, Apartment 999B, Floor 42"

# RTL
"١٢٣ شارع المثال، القاهرة، مصر"    # Arabic address

# PO Box
"PO Box 1234"

# No street number
"Corner of Main and Oak"

# Non-standard postal codes
"SW1A 1AA"      # UK
"75001"         # France
"100-0001"      # Japan
"EC1A 1BB"      # Complex UK format

# Missing components
""              # Empty
"N/A"           # Placeholder
```

---

## Passwords (for testing password fields only)

```
""                          # Empty
"a"                         # Single character
"password123"               # Common weak password
"P@ssw0rd!"                 # Meets typical complexity
"x" * 72                    # bcrypt max (72 bytes)
"x" * 73                    # Over bcrypt limit
"💀" * 20                   # Unicode/emoji password
" leading space"            # Leading whitespace
"trailing space "           # Trailing whitespace
```

---

## IDs and UUIDs

```
"00000000-0000-0000-0000-000000000000"  # Nil UUID
"ffffffff-ffff-ffff-ffff-ffffffffffff"  # Max UUID
"not-a-uuid"                            # Invalid format
""                                      # Empty
"0"                                     # Integer zero as ID
"-1"                                    # Negative ID
"999999999999"                          # Very large integer ID
```