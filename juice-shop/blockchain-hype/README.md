# Blockchain Hype

## Challenge

**OWASP Juice Shop — Blockchain Hype**

The challenge was solved in a local Docker instance of OWASP Juice Shop.

## Objective

Find and decode the encrypted announcement containing information about the upcoming token sale.

## Discovery

The Juice Shop `robots.txt` revealed a disallowed `/ftp` path:

```text
Disallow: /ftp
```

Browsing the directory exposed several files, including:

```text
announcement_encrypted.md
encrypt.pyc
```

The encrypted announcement contained many very large integers instead of readable text.

## Analysis

The `encrypt.pyc` file was identified as a **Python 2.7 byte-compiled file**.

Disassembling the bytecode revealed:

* RSA modulus `N`
* Public exponent `e = 65537`
* Each character was encrypted individually using:

```python
pow(ord(char), e, N)
```

The RSA modulus was 1024 bits.

Because each plaintext character was encrypted independently, the ciphertext could be matched against the RSA encryption of possible byte values.

## Decryption

I generated RSA ciphertext values for all possible byte values and created a lookup table.

Each integer from `announcement_encrypted.md` was then matched against this table.

The result was fully decoded with **0 unknown characters**.

The decrypted announcement contained:

> Major Announcement:
> Token Sale - Initial Coin Offering

It also contained the token-sale URL:

```text
/#/tokensale-ico-ea
```

## Result

The decrypted announcement led to the **Token Sale / Juicycoin** page.

The Juice Shop challenge confirmed:

**Blockchain Hype — Successfully Solved**

## Key Takeaways

* `robots.txt` can reveal interesting application paths.
* Exposed files can provide valuable information during security testing.
* Bytecode can reveal the logic used to protect sensitive data.
* RSA becomes insecure when used incorrectly, such as encrypting a tiny plaintext domain independently with a deterministic scheme.

## Evidence

The original `encrypt.pyc` file used during the analysis is included in this repository.

**Environment:** Kali Linux + Docker
**Target:** OWASP Juice Shop
**Challenge:** Blockchain Hype
