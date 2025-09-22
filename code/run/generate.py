import argparse, os, re, json
from .utils_io import write_json, sha1_text, now_ts
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',required=True); ap.add_argument('--tasks',required=True)
    ap.add_argument('--prompts',required=True); ap.add_argument('--out',required=True)
    ap.add_argument('--subset'); ap.add_argument('--max-samples',type=int); ap.add_argument('--dry-run',action='store_true')
    a=ap.parse_args(); os.makedirs(a.out,exist_ok=True)
    n=a.max_samples or 3
    for i in range(1,n+1):
        tid=f"task_{i:03d}"
        if a.subset and not re.search(a.subset, tid): continue
        art=os.path.join(a.out,f"{tid}.pv"); meta=os.path.join(a.out,f"{tid}.meta.json")
        if not a.dry-run:
            with open(art,'w',encoding='utf-8') as f: f.write(f"/* placeholder {tid} by {a.model} */\n")
            write_json(meta, {"model":a.model,"prompt_hash":sha1_text(tid),"ts":now_ts(),"params":{"temperature":0}})
    print(json.dumps({"written":n,"out":a.out},indent=2))
if __name__=='__main__': main()
