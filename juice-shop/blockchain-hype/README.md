# OWASP Juice Shop — Blockchain Hype

> **Challenge:** Blockchain Hype
> **Platform:** OWASP Juice Shop
> **Category:** Confidential Document / Cryptography
> **Environment:** Kali Linux + Docker
> **Status:** Solved

## 1. What I did

I solved the **Blockchain Hype** challenge in OWASP Juice Shop. The goal was to find a confidential announcement before it was officially released.

I found an FTP directory with several files. Two of them looked especially interesting: an encrypted announcement and a Python bytecode file that was related to the encryption.

My plan was to figure out how the encryption worked, get the needed values, decrypt the announcement, and then open the hidden Token Sale page.

---

## 2. Setting up the lab

I ran Juice Shop locally with Docker:

```bash
sudo docker run -d \
  --name juice-shop \
  -p 3000:3000 \
  bkimminich/juice-shop
```

The application was accessible at:

```text
http://127.0.0.1:3000
```

I verified that the container was running:

```bash
sudo docker ps
```

---

## 3. Finding the FTP directory

I checked the `/ftp/` directory:

Requesting:

```text
http://127.0.0.1:3000/ftp/
```

revealed several files:

```text
quarantine
acquisitions.md
announcement_encrypted.md
coupons_2013.md.bak
eastere.gg
encrypt.pyc
incident-support.kdbx
legal.md
package-lock.json.bak
package.json.bak
suspicious_errors.yml
```

The two files that caught my attention were:

```text
announcement_encrypted.md
encrypt.pyc
```

The first contained a lot of large numbers, and the second was a Python `.pyc` file, so I suspected it contained the encryption code.

---

## 4. Looking at the encrypted file

The announcement could be retrieved with:

```bash
curl -s http://127.0.0.1:3000/ftp/announcement_encrypted.md
```

Instead of normal text, I got a lot of very large integers.

I analyzed the structure:

```bash
curl -s http://127.0.0.1:3000/ftp/announcement_encrypted.md | python3 -c '
import sys
nums=[x for x in sys.stdin.read().split() if x.isdigit()]
print("Total:", len(nums))
print("Unique:", len(set(nums)))
print("Repeated:", len(nums) - len(set(nums)))
'
```

Output:

```text
Total: 1194
Unique: 43
Repeated: 1151
```

There were only 43 unique values out of 1194 numbers. That made me think the same plaintext characters were producing the same ciphertext values.

So I suspected that the file was encrypted one character at a time.

---

## 5. Getting the encryption code

At first I looked for `encrypt.pyc` in the wrong path inside the container, so I checked the Docker filesystem instead.

I therefore inspected the Docker image filesystem:

```bash
sudo docker export juice-shop | tar -t | grep -E 'encrypt\.pyc|announcement_encrypted\.md'
```

That showed:

```text
juice-shop/ftp/announcement_encrypted.md
juice-shop/ftp/encrypt.pyc
```

I then copied the bytecode to my Desktop:

```bash
sudo docker cp \
  juice-shop:/juice-shop/ftp/encrypt.pyc \
  ~/Desktop/encrypt.pyc
```

---

## 6. Checking the Python version

Running:

```bash
file ~/Desktop/encrypt.pyc
```

returned:

```text
python 2.7 byte-compiled
```

The file was compiled for Python 2.7, so I used Python 2.7 to inspect it.

```bash
python2 --version
```

---

## 7. Reading the bytecode

My first attempt with `python3 -m dis` failed. I also tried the normal Python 2 `dis` command, but that did not work either. I ended up loading the `.pyc` with `marshal` and then passing the code object to `dis`.

Instead, the bytecode was loaded manually with `marshal`:

```bash
python2 -c '
import marshal,dis
f=open("/home/ciel/Desktop/encrypt.pyc","rb")
f.read(8)
code=marshal.load(f)
dis.dis(code)
'
```

The important part of the output showed:

```python
N = 145906768007583323230186939349070635292401872375357164399581871019873438799005358938369571402670149802121818086292467422828157022922076746906543401224889672472407926969987100581290103199317858753663710862357656510507883714297115637342788911463535102712032765166518411726859837988672111837205085526346618740053

e = 65537
```

The most important line was:

```python
pow(ord(char), e, N)
```

That was basically the whole clue I needed.

---

## 8. Realizing it was RSA

The expression:

```python
pow(m, e, N)
```

is the usual form of RSA encryption:

```text
c = m^e mod N
```

where:

* `m` = plaintext character value
* `e` = public exponent
* `N` = RSA modulus
* `c` = ciphertext

The recovered public parameters were:

```text
e = 65537
N = 1024-bit RSA modulus
```

So the bytecode gave me the public RSA values I needed to reproduce the same calculation.

---

## 9. Decrypting it

The important thing was that the program encrypts:

```python
ord(char)
```

Each character is therefore just a small integer.

I did not need to factor the 1024-bit RSA modulus. Since there are only 256 possible byte values, I calculated the RSA result for every possible value:

```python
lookup = {}

for i in range(256):
    lookup[pow(i, e, N)] = i
```

This gave me a lookup table:

```text
RSA ciphertext → original character
```

I downloaded the encrypted announcement and matched every number against that table.

I put the same process into:

```text
decrypt.py
```

This worked because the application was encrypting **individual small character values** instead of using RSA properly with padding.

---

## 10. What I got

The output finally became readable. It started with:

```text
Major Announcement:

Token Sale - Initial Coin Offering
```

The decrypted document eventually revealed:

```text
URL: /#/tokensale-ico-ea
```

This gave me the route to the hidden Token Sale page.

---

## 11. Opening the hidden page

Navigating to:

```text
/#/tokensale-ico-ea
```

opened the Juicycoin Token Sale page.

Juice Shop then showed:

```text
You successfully solved a challenge:
Blockchain Hype
```

So the challenge was successfully solved.

---

## 12. Screenshots I would include

For my GitHub write-up, I would include these screenshots:

### Screenshot 1 — FTP Directory

Show the `/ftp/` directory containing:

```text
announcement_encrypted.md
encrypt.pyc
```

### Screenshot 2 — Encrypted Announcement

Show the large integer ciphertext.

### Screenshot 3 — Python Bytecode

Show the disassembly containing:

```text
N
e = 65537
pow(...)
```

### Screenshot 4 — Decryption

Show the terminal output containing:

```text
Unknown: 0
```

and the beginning of the decrypted announcement.

### Screenshot 5 — Challenge Completion

Show the Juice Shop page displaying:

```text
You successfully solved a challenge:
Blockchain Hype
```

---

## 13. What I learned

This challenge helped me practice several things:

* Sensitive files accidentally exposed through a web-accessible directory
* Information disclosure through backup and auxiliary files
* Python bytecode analysis
* Reverse engineering a simple encryption implementation
* RSA public-key cryptography
* Why textbook RSA is unsafe for encrypting individual messages
* The importance of proper padding and secure cryptographic design
* How seemingly harmless metadata/files can reveal the mechanism behind protected data

### Main lesson

The interesting part was that the RSA key itself was not the main problem.

The problem was **how RSA was being used**.

The application encrypted each character independently:

```python
pow(ord(char), e, N)
```

Since the plaintext space was extremely small, the encryption could be reproduced for every possible character and reversed using a lookup table.

For me, the main takeaway was:

> Strong cryptographic primitives can still become insecure when they are implemented or used incorrectly.

---

## 14. Tools I used

```text
Kali Linux
Docker
OWASP Juice Shop
curl
Python 2.7
Python 3
marshal
dis
RSA mathematics
```

---

## 15. Result

**Challenge:** Blockchain Hype

**Result:** Successfully solved

**Attack chain:**

```text
FTP Discovery
      ↓
Encrypted Announcement
      ↓
encrypt.pyc Discovery
      ↓
Python 2.7 Bytecode Analysis
      ↓
Recover N and e
      ↓
Recognize RSA
      ↓
Build Character Encryption Lookup
      ↓
Decrypt Announcement
      ↓
Discover Hidden Route
      ↓
Token Sale Page
      ↓
Challenge Solved 
```

---

## Disclaimer

This write-up documents testing performed against a deliberately vulnerable **OWASP Juice Shop** instance running locally in a controlled lab environment.

No third-party or production systems were targeted.
