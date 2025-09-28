# dsa/dsa_compare.py
import json, time, random
from pathlib import Path

DATA_PATH = Path('dsa/transactions.json')

def linear_search(data, target_id):
    for item in data:
        if item.get('id') == target_id:
            return item
    return None

def dict_lookup(d, target_id):
    return d.get(target_id)

def main():
    data = json.load(DATA_PATH.open('r', encoding='utf8'))
    ids = [item['id'] for item in data]
    sample_ids = random.sample(ids, min(20, len(ids)))

    # build dict
    d = {item['id']: item for item in data}

    # measure linear
    t0 = time.perf_counter()
    for tid in sample_ids:
        linear_search(data, tid)
    t1 = time.perf_counter()
    linear_time = t1 - t0

    # measure dict
    t0 = time.perf_counter()
    for tid in sample_ids:
        dict_lookup(d, tid)
    t1 = time.perf_counter()
    dict_time = t1 - t0

    print('sample_count=', len(sample_ids))
    print(f'Linear search total time: {linear_time:.6f} s')
    print(f'Dict lookup total time:   {dict_time:.6f} s')
    print('Per-op approx: linear {:.6f} ms, dict {:.6f} ms'.format(
        linear_time/len(sample_ids)*1000, dict_time/len(sample_ids)*1000
    ))

if __name__ == '__main__':
    main()
