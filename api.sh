

curl -X 'POST' \
  'http://localhost:8000/api/bank-account/deposit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "67f4b900-c7a9-4e65-97e2-f3c0dfb44b07",
  "amount": "100.50"
}' | jq '.'



curl -X 'POST' \
  'http://localhost:8000/api/bank-account/overdraft/redraw' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "bfba8c1a-a3c1-40b9-9d36-6b25803e4f9f",
  "amount": "100.50"
}' | jq '.'


curl -X 'POST' \
  'http://localhost:8000/api/bank-account/overdraft/modify' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "bfba8c1a-a3c1-40b9-9d36-6b25803e4f9f",
  "amount": "2000.50"
}' | jq '.'



curl -X 'POST' \
  'http://localhost:8000/api/booklet-account/deposit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "f13057a4-021d-484a-9224-74d467657c91",
  "amount": "2000.50"
}' | jq '.'


curl -X 'POST' \
  'http://localhost:8000/api/booklet-account/redraw' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "f13057a4-021d-484a-9224-74d467657c91",
  "amount": "1000.50"
}' | jq '.'

curl -X 'POST' \
  'http://localhost:8000/api/booklet-account/deposit/limit' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "account_number": "f13057a4-021d-484a-9224-74d467657c91",
  "amount": "1000.50"
}' | jq '.'