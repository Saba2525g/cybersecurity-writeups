# Cybersecurity Writeups

Hands-on cybersecurity labs, CTF write-ups, and security research.

This repository documents practical security work, including the methodology, analysis, tools, and lessons learned from each challenge.

## Writeups

### OWASP Juice Shop

| Challenge                                                | Category                              | Status   |
| -------------------------------------------------------- | ------------------------------------- | -------- |
| [Blockchain Hype](juice-shop/blockchain-hype/)           | Cryptography / Information Disclosure |  Solved |
| [Retrieve Blueprint](juice-shop/retrieve-blueprint/)     | Sensitive Data Exposure               |  Solved |
| [Ephemeral Accountant](juice-shop/ephemeral-accountant/) | Injection                             |  Solved |

## Focus Areas

* Web Security
* Injection
* Information Disclosure
* Cryptography
* Reverse Engineering
* Python Bytecode Analysis
* Linux
* Docker
* CTF Methodology

## Environment

* Kali Linux
* Docker
* Python
* OWASP Juice Shop

## Repository Structure

```text
cybersecurity-writeups/
│
├── README.md
│
└── juice-shop/
    ├── blockchain-hype/
    │   ├── README.md
    │   ├── decrypt.py
    │   ├── encrypt.pyc
    │   └── images/
    │       └── blockchain-hype-solved.png
    │
    └── retrieve-blueprint/
        ├── README.md
        └── images/

    └── ephemeral-accountant/
        ├── README.md
        └── images/
```

## Disclaimer

All testing documented in this repository was performed against intentionally vulnerable applications in controlled lab environments.

No third-party or production systems were targeted.
