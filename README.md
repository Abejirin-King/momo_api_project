# MoMo REST API (assignment)

## Prereqs
- Python 3.10+
- (Optional) virtualenv

## Quickstart
1. Parse XML -> JSON:
   python dsa/parse_xml.py
   This creates dsa/transactions.json

2. Start API server:
   python api/server.py
   Server listens on port 8000.

3. Test with curl or Postman (see docs/api_docs.md).

## Files
- dsa/parse_xml.py : XML -> JSON
- dsa/dsa_compare.py : compares linear vs dict lookup timings
- api/server.py : simple REST server with Basic Auth
- docs/api_docs.md : API documentation

