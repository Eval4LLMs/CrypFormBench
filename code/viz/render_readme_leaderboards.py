import argparse, os, re
B=lambda k:f"<!-- LEADERBOARD_{k}:BEGIN -->"; E=lambda k:f"<!-- LEADERBOARD_{k}:END -->"
def replace_block(text,key,payload):
    pat=re.compile(re.escape(B(key))+".*?"+re.escape(E(key)),re.S)
    blk=f"{B(key)}\n{payload}\n{E(key)}"
    return re.sub(pat, blk, text) if re.search(pat,text) else (text+"\n\n"+blk+"\n")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--in',dest='indir',required=True); ap.add_argument('--readme',required=True)
    ap.add_argument('--blocks',nargs='+',required=True); ap.add_argument('--overwrite-blocks',action='store_true')
    a=ap.parse_args()
    with open(a.readme,'r',encoding='utf-8') as f: md=f.read()
    payload="Auto-generated placeholder table"
    for k in a.blocks: md=replace_block(md,k,payload)
    with open(a.readme,'w',encoding='utf-8') as f: f.write(md)
    print("Updated blocks:", ", ".join(a.blocks))
if __name__=='__main__': main()
