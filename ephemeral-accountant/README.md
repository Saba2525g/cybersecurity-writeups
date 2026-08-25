# OWASP Juice Shop — Ephemeral Accountant

> **Challenge:** Ephemeral Accountant  
> **Platform:** OWASP Juice Shop  
> **Category:** Injection  
> **Difficulty:** 5 Stars  
> **Environment:** Kali Linux + Docker  
> **Status:** Solved

## 1. Objective

Log in as the non-existing accountant:

`acc0unt4nt@juice-sh.op`

without ever registering that user.

The key idea is that the accountant must exist only temporarily as part of the SQL query result, rather than being created permanently in the database.

## 2. Initial Login Attempt

A normal login attempt with the target email and an incorrect password returned:

```text
401 Unauthorized
Invalid email or password.
