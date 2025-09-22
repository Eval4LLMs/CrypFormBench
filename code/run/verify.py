import argparse, os, glob, pathlib, yaml, json
from ..tools.adapters import proverif, tamarin, scyther, maude_npa, avispa, cryptoverif, easycrypt
from ..run.utils_io import write_json
MAP={'.pv':proverif,'.spthy':tamarin,'.if':avispa,'.maude':maude_npa,'.ocv':cryptoverif,'.ec':easycrypt,'.spdl':scyther}
def pick(ext): return MAP.get(ext, proverif)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',required=True); ap.add_argument('--tool-config',required=True)
    ap.add_argument('--out',required=True); ap.add_argument('--timeout-sec',type=int,default=None)
    ap.add_argument('--parallel',type=int,default=1); a=ap.parse_args()
    os.makedirs(a.out,exist_ok=True)
    with open(a.tool_config,'r',encoding='utf-8') as f: cfg=yaml.safe_load(f)
    arts=[p for p in glob.glob(os.path.join(a.inputs,'*.*')) if not p.endswith('.json')]
    w=0
    for p in arts:
        ext=pathlib.Path(p).suffix.lower(); ad=pick(ext)
        ver=ad.run(p, timeout=a.timeout_sec or 600, flags=[])
        base=os.path.join(a.out, pathlib.Path(p).stem)
        with open(base+'.log','w',encoding='utf-8') as f: f.write(f"[log for {os.path.basename(p)}]\n")
        write_json(base+'.verdict.json', ver); w+=1
    print(json.dumps({"verified":w,"out":a.out},indent=2))
if __name__=='__main__': main()
