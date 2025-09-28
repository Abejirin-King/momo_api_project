import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path

XML_PATH = Path('dsa/modified_sms_v2.xml')  
OUT_JSON = Path('dsa/transactions.json')

def normalize_body(body):
    return re.sub(r'\s+', ' ', body).strip()

def parse_sms_element(elem):
    sms = {
        'raw_attrs': elem.attrib,
        'address': elem.attrib.get('address'),
        'date_unix_ms': int(elem.attrib.get('date', '0')),
        'readable_date': elem.attrib.get('readable_date'),
        'service_center': elem.attrib.get('service_center'),
        'contact_name': elem.attrib.get('contact_name'),
    }
    body = elem.attrib.get('body', '')
    sms['body'] = normalize_body(body)

    tx = {}
    m = re.search(r'(TxId[:\s]*|Financial Transaction Id[:\s]*)?(\d{5,})', body)
    if m:
        tx['tx_id'] = m.group(2)

    m_amt = re.search(r'([0-9][0-9,\.]*\s*(?:RWF|RWF\.|RWF,|RWF))', body)
    if m_amt:
        amt = m_amt.group(1).replace(',', '').replace('.', '').replace('RWF','').strip()
        try:
            tx['amount'] = int(amt)
            tx['currency'] = 'RWF'
        except:
            tx['amount_raw'] = m_amt.group(1)

    if re.search(r'\breceived\b', body, re.I):
        tx['type'] = 'receive'
    elif re.search(r'\bwithdrawn\b', body, re.I):
        tx['type'] = 'withdraw'
    elif re.search(r'\bdeposit\b', body, re.I):
        tx['type'] = 'deposit'
    elif re.search(r'\bpayment\b|\btransferred\b|\bYour payment of\b', body, re.I):
        tx['type'] = 'payment'
    else:
        tx['type'] = 'unknown'

    m_name_num = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+).*?(\(?250[0-9]{7,}\)?)', body)
    if m_name_num:
        tx['name'] = m_name_num.group(1)
        tx['phone'] = m_name_num.group(2)
    else:
        m_name = re.search(r'from\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', body, re.I)
        if m_name:
            tx['name'] = m_name.group(1).strip()

    sms['transaction'] = tx
    return sms

def parse_all():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    transactions = []
    next_id = 1
    for sms in root.findall('sms'):
        item = parse_sms_element(sms)
        item['id'] = next_id
        next_id += 1
        transactions.append(item)
    return transactions

def main():
    transactions = parse_all()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open('w', encoding='utf8') as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    print(f'Parsed {len(transactions)} sms into {OUT_JSON}')

if __name__ == '__main__':
    main()
