import hashlib, json, os, time
def sha1_text(s): return hashlib.sha1(s.encode()).hexdigest()
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2)
def now_ts(): return int(time.time())
