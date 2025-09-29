# MoMo Transactions API

Base URL: http://<host>:8000/

## Authentication
All endpoints require HTTP Basic Authentication.
Example header:
Authorization: Basic base64(student:password123)

If credentials are missing/invalid → 401 Unauthorized (WWW-Authenticate header present).

## Endpoints

### GET /transactions
List all transactions.
Request:
  GET /transactions
Response (200):
  [ { id: 1, raw_attrs: {...}, address: "M-Money", transaction: {...} }, ... ]
Errors:
  401 Unauthorized

### GET /transactions/{id}
Get single transaction.
Request:
  GET /transactions/123
Response (200):
  { id:123, ... }
Errors:
  401 Unauthorized
  404 Not Found
  400 Invalid id

### POST /transactions
Create new transaction.
Request:
  POST /transactions
  Body (JSON): transaction object to add (server will set `id`)
Response (201):
  Created object with id
Errors:
  401 Unauthorized
  400 Invalid JSON

### PUT /transactions/{id}
Update transaction with ID.
Request:
  PUT /transactions/123
  Body: full JSON object (id will be set to 123)
Response (200): updated object
Errors:
  401, 400, 404

### DELETE /transactions/{id}
Delete transaction.
Request:
  DELETE /transactions/123
Response (200): { "deleted": 123 }
Errors:
  401, 400, 404

## Examples (curl)

1) List (authorized):
curl -u student:password123 http://localhost:8000/transactions

2) Unauthorized:
curl http://127.0.0.1:8000/transactions

3) Get:
curl -u student:password123 http://127.0.0.1:8000/transactions/1

4) Create:
curl -u student:password123 -X POST http://127.0.0.1:8000/transactions -H "Content-Type: application/json" -d '{"address":"M-Money","transaction": {"type":"test","amount":10}}'

5) Update:
curl -u student:password123 -X PUT http://127.0.0.1:8000/transactions/2 -H "Content-Type: application/json" -d '{"address":"M-Money","transaction": {"type":"updated","amount":20}}'

6) Delete:
curl -u student:password123 -X DELETE http://127.0.0.1:8000/transactions/1
