# Forged Feedback

> **Challenge:** Forged Feedback
> **Platform:** OWASP Juice Shop
> **Category:** Broken Access Control
> **Difficulty:** 3 Star
> **Status:** Solved

## 1. Overview

The objective of this challenge is to post feedback in another user's name.

The vulnerability is caused by improper access control when creating feedback. The server accepts a client-supplied `UserId` instead of reliably determining the owner from the authenticated session.

---

## 2. Reconnaissance

I first inspected the Feedback API:

```bash
curl -s http://localhost:3000/api/Feedbacks | head -c 2000
```

The endpoint returned feedback objects containing a `UserId` field:

```json
{
  "UserId": 1,
  "id": 1,
  "comment": "I love this shop! Best products in town! Highly recommended!",
  "rating": 5
}
```

This showed that feedback records are associated with specific users.

The important observation was that `UserId` appeared to be part of the API data model.

---

## 3. Testing the API

I then tested whether the `UserId` could be controlled when creating a new feedback entry.

The following request was sent:

```bash
curl -s -X POST http://localhost:3000/api/Feedbacks \
  -H "Content-Type: application/json" \
  -d '{"comment":"Forged feedback test","rating":5,"UserId":1}'
```

The request was accepted successfully.

The important part of the request was:

```json
"UserId":1
```

Instead of the server determining the owner from the authenticated user, the client was able to provide the user identifier.

---

## 4. Exploitation

By supplying another user's `UserId`, I was able to create a feedback entry associated with that user.

The vulnerable flow can be represented as:

```text
Client
  |
  | POST /api/Feedbacks
  | UserId = 1
  v
Server
  |
  | trusts client-supplied UserId
  v
Feedback associated with User 1
```

This demonstrates broken access control because the application does not properly enforce ownership of the newly created feedback.

---

## 5. Evidence

The successful request and response were captured as evidence:

![Forged Feedback solved](images/solved.png)

---

## 6. Root Cause

The underlying issue is that the application trusts a security-sensitive value supplied directly by the client.

A secure implementation should derive the user identity from the authenticated session instead of accepting an arbitrary `UserId` from the request body.

Conceptually:

```text
Insecure:

Client → UserId → Server → create feedback


Secure:

Authenticated Session → Server determines UserId → create feedback
```

---

## 7. Security Impact

An attacker could potentially create feedback that appears to belong to another user.

Depending on how the affected user identity is used elsewhere in the application, this could lead to:

* Impersonation of another user's actions
* Integrity loss in feedback records
* Misattribution of user-generated content
* Abuse of trust in application data

---

## 8. Mitigation

The server should not trust `UserId` values supplied by the client.

Instead:

1. Authenticate the user.
2. Obtain the user's identity from the server-side session or authentication token.
3. Ignore or reject client-supplied ownership fields.
4. Assign the authenticated user's ID server-side.
5. Enforce authorization checks whenever feedback records are created or modified.

For example:

```text
Authenticated User
        |
        v
   Server-side
   identity
        |
        v
   Create Feedback
        |
        v
   UserId assigned
   by the server
```

---

## 9. Conclusion

The challenge was solved by identifying that the Feedback API trusted a client-controlled `UserId`.

By modifying this value in the request body, I was able to create feedback associated with another user, demonstrating a Broken Access Control vulnerability.
